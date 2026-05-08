# token refresh route
from fastapi import APIRouter, Response, HTTPException
from fastapi import Request
from app.services.auth.tokens import create_access_token
from app.core.config import settings
from jose import jwt, JWTError

router = APIRouter(tags=["auth"])

@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # new access token
    new_access_token = create_access_token(subject=payload["sub"])

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.cookie_samesite,
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        path="/",
    )

    return {"message": "Access token refreshed"}
