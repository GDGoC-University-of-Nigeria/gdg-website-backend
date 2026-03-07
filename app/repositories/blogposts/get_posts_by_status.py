from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.blogpost import BlogPost, BlogPostStatus


async def get_posts_by_status(
    db: AsyncSession,
    status: BlogPostStatus | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[BlogPost]:
    query = select(BlogPost).order_by(BlogPost.posted_at.desc()).offset(skip).limit(limit)
    if status is not None:
        query = query.where(BlogPost.status == status)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_posts_by_status_with_author(
    db: AsyncSession,
    status: BlogPostStatus | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[BlogPost]:
    """List blog posts with author relationship loaded (for admin list)."""
    query = (
        select(BlogPost)
        .options(selectinload(BlogPost.author))
        .order_by(BlogPost.posted_at.desc())
        .offset(skip)
        .limit(limit)
    )
    if status is not None:
        query = query.where(BlogPost.status == status)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_author_posts(
    db: AsyncSession,
    author_id: UUID,
    skip: int = 0,
    limit: int = 50,
) -> list[BlogPost]:
    result = await db.execute(
        select(BlogPost)
        .where(BlogPost.author_id == author_id)
        .order_by(BlogPost.posted_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())
