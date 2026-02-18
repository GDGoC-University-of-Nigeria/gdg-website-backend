"""POST /api/v1/blogposts — Submit a blog post (authenticated users)."""

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.blogposts import create_blogpost
from app.schemas.blogpost import BlogPostCreate, BlogPostRead
from .router import router


@router.post("/", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
async def submit_blogpost(
    payload: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit a new blog post.

    - Available to all authenticated users (including admins).
    - **Admin posts are auto-approved** and immediately publicly visible.
    - Regular user posts are created with **status = pending**.
    """
    return await create_blogpost(
        db=db,
        payload=payload,
        author_id=current_user.id,
        auto_approve=current_user.is_admin,
    )

