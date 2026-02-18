"""PATCH /api/v1/admin/blogposts/{id}/approve — Admin: approve a blog post."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.blogpost import BlogPostStatus
from app.models.user import User
from app.repositories.blogposts import approve_blogpost, get_blogpost_by_id
from app.schemas.blogpost import BlogPostAdminRead
from .router import router


@router.patch("/{post_id}/approve", response_model=BlogPostAdminRead)
async def approve_post(
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Approve a pending blog post.

    - Only admins can approve.
    - An admin **cannot** approve their own post.
    - Only `pending` posts can be approved.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post.author_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot approve their own posts",
        )

    if post.status != BlogPostStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve a post with status '{post.status.value}'",
        )

    return await approve_blogpost(db=db, post=post, admin_id=current_admin.id)
