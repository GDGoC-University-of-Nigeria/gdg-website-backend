from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user_by_provider_id(
    db: AsyncSession, provider: str, provider_user_id: str
) -> Optional[User]:
    from sqlalchemy.orm import selectinload
    stmt = select(User).options(selectinload(User.profile)).where(
        User.provider == provider,
        User.provider_user_id == provider_user_id,
    )
    result = await db.execute(stmt)
    return result.scalars().first()

