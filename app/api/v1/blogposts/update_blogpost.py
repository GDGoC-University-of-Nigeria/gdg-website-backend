"""PATCH /api/v1/blogposts/{post_id} — Author edit (only while pending)."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.blogpost import BlogPostStatus
from app.models.user import User
from app.repositories.blogposts import get_blogpost_by_id, update_blogpost
from app.schemas.blogpost import BlogPostRead, BlogPostUpdate
from .router import router


@router.patch("/{post_id}", response_model=BlogPostRead)
async def author_update_blogpost(
    payload: BlogPostUpdate,
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Edit a blog post's content.

    - Only the **author** can edit.
    - Editing is only allowed while the post is in **pending** status.
      Once approved or rejected, the post is locked for the author.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own posts",
        )

    if post.status != BlogPostStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Posts can only be edited while they are pending review",
        )

    return await update_blogpost(db=db, post=post, payload=payload)
