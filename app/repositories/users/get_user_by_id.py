from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_id(
    db: AsyncSession,
    user_id: UUID,
) -> Optional[User]:
    from sqlalchemy.orm import selectinload
    stmt = select(User).options(selectinload(User.profile)).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

