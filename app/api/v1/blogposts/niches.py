"""GET /api/v1/blogposts/niches — Public list of distinct blog niches."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import get_db
from app.models.blogpost import BlogPost, BlogPostStatus
from .router import router


@router.get("/niches", response_model=list[str])
async def list_niches(db: AsyncSession = Depends(get_db)):
    """
    Return a sorted list of distinct niche values from all approved blog posts.
    Useful as a dropdown data source on the frontend.
    No authentication required.
    """
    result = await db.execute(
        select(BlogPost.niche)
        .distinct()
        .where(
            BlogPost.niche.is_not(None),
            BlogPost.status == BlogPostStatus.approved,
        )
        .order_by(BlogPost.niche.asc())
    )
    return [row[0] for row in result.all()]
