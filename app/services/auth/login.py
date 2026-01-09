from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import get_user_by_email
from app.core.security import verify_password


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, cast(str, user.hashed_password)):
        return None

    return user

