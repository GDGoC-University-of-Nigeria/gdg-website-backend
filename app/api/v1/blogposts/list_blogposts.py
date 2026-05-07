"""GET /api/v1/blogposts — Public listing of approved posts."""

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.blogposts import get_all_approved
from app.schemas.blogpost import BlogPostRead
from .router import router


@router.get("/", response_model=list[BlogPostRead])
async def list_approved_blogposts(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List all approved blog posts.

    - Public endpoint — no authentication required.
    - Ordered by approval date (newest first).
    """
    return await get_all_approved(db=db, skip=skip, limit=limit)
