"""Get non-admin community members with pagination."""
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_community_members(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
) -> List[User]:
    """Return non-admin users, ordered by created_at desc, with pagination."""
    from sqlalchemy.orm import selectinload
    stmt = (
        select(User)
        .options(selectinload(User.profile))
        .where(User.is_admin == False)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())
