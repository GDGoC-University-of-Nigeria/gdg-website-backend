from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    from sqlalchemy.orm import selectinload
    stmt = select(User).options(selectinload(User.profile)).where(User.email == email)
    result = await db.execute(stmt)

    return result.scalars().first()
