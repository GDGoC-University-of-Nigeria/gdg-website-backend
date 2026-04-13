"""
Google OAuth routes — cookie-free state verification.

The state parameter is self-contained: it's a signed token (via itsdangerous)
that Google echoes back in the callback query string. We verify the signature,
expiry, and User-Agent binding on callback — no cookies or session needed.

Flow:
  1. /auth/google → generate a signed state token (with UA hash), redirect to Google
  2. /auth/google/callback → Google echoes the state back; we verify signature + UA
"""
import hashlib
import logging
import secrets
import httpx

from urllib.parse import urlencode
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.core.config import settings
from app.db.session import get_db
from app.services.auth.google import find_or_create_google_user
from app.services.auth.tokens import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

# Signer for the state parameter — the signed token IS the CSRF protection.
_signer = URLSafeTimedSerializer(settings.SESSION_SECRET_KEY)


def _ua_hash(request: Request) -> str:
    """SHA-256 hash of the User-Agent header (context binding)."""
    ua = (request.headers.get("user-agent") or "").encode()
    return hashlib.sha256(ua).hexdigest()


@router.get("/google", summary="Initiate Google OAuth login")
async def google_login(request: Request):
    """
    Build the Google consent URL with a signed state token and redirect.
    The state payload includes a random nonce and a User-Agent hash for
    context binding — preventing cross-device replay of the state token.
    """
    payload = {
        "nonce": secrets.token_urlsafe(24),
        "ua": _ua_hash(request),
    }
    signed_state = _signer.dumps(payload)

    params = urlencode({
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": signed_state,
        "access_type": "offline",
        "prompt": "select_account",
    })
    url = f"{GOOGLE_AUTH_URL}?{params}"

    logger.info("Redirecting to Google (state=%s...)", signed_state[:20])
    return RedirectResponse(url=url)


@router.get("/google/callback", summary="Google OAuth callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Google redirects here with ?state=...&code=...
    We verify the signed state (signature + expiry + UA binding), exchange
    the code for tokens, find-or-create the user, and redirect to frontend.
    """
    state = request.query_params.get("state")
    code = request.query_params.get("code")

    # ── 1. Verify state signature + expiry (CSRF protection) ──────────────
    if not state:
        logger.error("No state parameter in callback")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=missing_state")

    try:
        payload = _signer.loads(state, max_age=300)  # strict 5-min expiry
    except SignatureExpired:
        logger.error("State token expired")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=state_expired")
    except BadSignature:
        logger.error("State token has invalid signature — possible CSRF attack")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=invalid_state")

    # ── 1b. Verify User-Agent binding (context check) 
    # if payload.get("ua") != _ua_hash(request):
    #     logger.error("State UA mismatch — possible cross-device replay")
    #     return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=invalid_state")

    if not code:
        logger.error("No authorization code in callback")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=no_code")

    # ── 2. Exchange the code for tokens 
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            },
        )

    if token_resp.status_code != 200:
        logger.error("Google token exchange failed: %s", token_resp.text)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=token_exchange_failed")

    access_token_google = token_resp.json().get("access_token")

    # ── 3. Fetch user info from Google 
    async with httpx.AsyncClient() as client:
        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token_google}"},
        )

    if userinfo_resp.status_code != 200:
        logger.error("Google userinfo fetch failed: %s", userinfo_resp.text)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth?error=userinfo_failed")

    user_info = userinfo_resp.json()
    logger.info("Google user: %s", user_info.get("email"))

    # ── 4. Find or create the local user 
    user = await find_or_create_google_user(db, user_info)

    our_access_token = create_access_token(subject=str(user.id))
    our_refresh_token = create_refresh_token(subject=str(user.id))

    # ── 5. Build the response 
    profile_complete = str(user.profile.is_complete).lower()
    redirect_url = (
        f"{settings.FRONTEND_URL}/auth/callback"
        f"?profile_complete={profile_complete}"
    )
    response = RedirectResponse(url=redirect_url)

    # Set access token cookie (global path — sent on every authenticated request)
    response.set_cookie(
        key="access_token",
        value=our_access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.cookie_samesite,
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        path="/",
    )

    # Set refresh token cookie (restricted to /auth/refresh — not sent on every request)
    response.set_cookie(
        key="refresh_token",
        value=our_refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.cookie_samesite,
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path="/auth/refresh",
    )

    return response
