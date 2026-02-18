from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.blogpost import BlogPost


async def get_blogpost_by_id(
    db: AsyncSession,
    post_id: UUID,
) -> BlogPost | None:
    result = await db.execute(
        select(BlogPost).where(BlogPost.id == post_id)
    )
    return result.scalar_one_or_none()
