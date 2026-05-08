"""PATCH /api/v1/admin/blogposts/{post_id} — Admin edit on behalf of author."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.blogposts import get_blogpost_by_id, update_blogpost
from app.schemas.blogpost import BlogPostAdminRead, BlogPostUpdate
from .router import router


@router.patch("/{post_id}", response_model=BlogPostAdminRead)
async def admin_update_blogpost(
    payload: BlogPostUpdate,
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Admin edit on behalf of the author.

    - Admins can edit any post regardless of status (pending, approved, rejected).
    - Does **not** reset the post status — use approve/reject for that.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    return await update_blogpost(db=db, post=post, payload=payload)
