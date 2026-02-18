"""GET /api/v1/blogposts/{id} — Fetch a single post with visibility rules."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.blogpost import BlogPostStatus
from app.models.user import User
from app.repositories.blogposts import get_blogpost_by_id
from app.schemas.blogpost import BlogPostAdminRead, BlogPostRead
from .router import router


@router.get("/{post_id}", response_model=BlogPostRead | BlogPostAdminRead)
async def get_blogpost(
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    """
    Fetch a single blog post by ID.

    - **Approved** → publicly accessible (no auth required).
    - **Pending / Rejected** → only the author or an admin can view.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post.status == BlogPostStatus.approved:
        return post

    # Non-public post: require auth and check ownership or admin
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    if not current_user.is_admin and post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return post
