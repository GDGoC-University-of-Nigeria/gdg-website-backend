"""Get non-admin community members with pagination and optional text search."""

from typing import Tuple, List

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, join

from app.models.user import User
from app.models.user_profile import UserProfile


async def get_community_members(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    q: str | None = None,
) -> Tuple[int, List[User]]:
    """
    Return (total_count, page_of_users) for non-admin members.

    If `q` is provided, filters by full_name (profile) or email containing
    the search string (case-insensitive).
    """
    base_filter = [User.is_admin == False]

    if q:
        search = f"%{q.strip()}%"
        base_filter.append(
            or_(
                User.email.ilike(search),
                UserProfile.full_name.ilike(search),
            )
        )

    # Total count query
    count_stmt = (
        select(func.count(User.id))
        .outerjoin(User.profile)
        .where(*base_filter)
    )
    total: int = (await db.execute(count_stmt)).scalar_one()

    # Paginated data query
    data_stmt = (
        select(User)
        .options(selectinload(User.profile))
        .outerjoin(User.profile)
        .where(*base_filter)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(data_stmt)
    users = list(result.scalars().all())

    return total, users
