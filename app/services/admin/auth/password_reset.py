from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password


async def reset_user_password(db: AsyncSession, email: str, new_password: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise ValueError("User not found")

    user.hashed_password = hash_password(new_password)
    await db.commit()
