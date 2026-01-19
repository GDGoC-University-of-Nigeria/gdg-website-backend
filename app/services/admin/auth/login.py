from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import verify_password
from app.services.auth.tokens import create_access_token, create_refresh_token


async def admin_login(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not user.hashed_password:
        raise ValueError("Invalid credentials")

    if not user.is_admin:
        raise PermissionError("Admin access required")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    access_token = create_access_token(
        subject=str(user.id),
        additional_claims={"is_admin": True}
    )

    refresh_token = create_refresh_token(
        subject=str(user.id),
        additional_claims={"is_admin": True}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
