from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth.login import LoginRequest
from app.services.auth.login import authenticate_user
from app.services.auth.tokens import create_access_token, create_refresh_token
from app.db.session import get_db
from app.core.config import settings

router = APIRouter(prefix="/api/v1/admin/auth", tags=["Admin Auth"])


@router.post("/login")
async def admin_login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(payload.email, payload.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    access_token = create_access_token(
        subject=str(user.id),
        additional_claims={"is_admin": True},
    )

    refresh_token = create_refresh_token(
        subject=str(user.id),
        additional_claims={"is_admin": True},
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        # samesite="lax",
        samesite="none",
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        # samesite="lax",
        samesite="none",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path="/api/v1/auth/refresh", 
    )

    return {"message": "Admin login successful"}
