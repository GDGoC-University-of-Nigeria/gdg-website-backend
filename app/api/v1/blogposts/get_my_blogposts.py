"""GET /api/v1/blogposts/me — Author's own posts (all statuses)."""

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.blogposts import get_author_posts
from app.schemas.blogpost import BlogPostAdminRead
from .router import router


@router.get("/me", response_model=list[BlogPostAdminRead])
async def get_my_blogposts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    Get the current user's own blog posts (all statuses).

    - Requires authentication.
    - Returns pending, approved, and rejected posts for the author.
    """
    return await get_author_posts(db=db, author_id=current_user.id, skip=skip, limit=limit)
