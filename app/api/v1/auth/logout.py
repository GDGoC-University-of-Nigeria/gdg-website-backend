from fastapi import APIRouter, Response

from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="none",
        secure=settings.COOKIE_SECURE,
    )
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh",
        samesite="none",
        secure=settings.COOKIE_SECURE,
    )
    return {"message": "Logged out successfully"}
