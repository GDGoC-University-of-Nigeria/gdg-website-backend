"""PATCH /api/v1/admin/blogposts/{id}/reject — Admin: reject a blog post."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.blogpost import BlogPostStatus
from app.models.user import User
from app.repositories.blogposts import get_blogpost_by_id, reject_blogpost
from app.schemas.blogpost import BlogPostAdminRead, BlogPostReject
from .router import router


@router.patch("/{post_id}/reject", response_model=BlogPostAdminRead)
async def reject_post(
    payload: BlogPostReject,
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Reject a pending blog post.

    - Only admins can reject.
    - Only `pending` posts can be rejected.
    - An optional `rejection_reason` can be provided.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post.status != BlogPostStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject a post with status '{post.status.value}'",
        )

    return await reject_blogpost(db=db, post=post, rejection_reason=payload.rejection_reason)
