from fastapi import APIRouter, Response

from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/logout")
def logout(response: Response):
    # Clear access token (global path)
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite=settings.cookie_samesite,
        secure=settings.COOKIE_SECURE,
        httponly=True,
    )
    # Clear refresh token (restricted path)
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh",
        samesite=settings.cookie_samesite,
        secure=settings.COOKIE_SECURE,
        httponly=True,
    )
    return {"message": "Logged out successfully"}
