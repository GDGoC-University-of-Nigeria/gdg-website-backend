from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blogpost import BlogPost, BlogPostStatus


async def get_all_approved(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
) -> list[BlogPost]:
    result = await db.execute(
        select(BlogPost)
        .where(BlogPost.status == BlogPostStatus.approved)
        .order_by(BlogPost.approved_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())
