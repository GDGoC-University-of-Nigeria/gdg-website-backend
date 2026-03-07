from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.comment import Comment


async def get_comments(
    db: AsyncSession,
    blogpost_id: UUID,
    skip: int = 0,
    limit: int = 20,
) -> list[Comment]:
    result = await db.execute(
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.blogpost_id == blogpost_id)
        .order_by(Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_comment_by_id(
    db: AsyncSession,
    comment_id: UUID,
) -> Comment | None:
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    return result.scalar_one_or_none()
