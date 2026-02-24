"""POST /api/v1/blogposts/{id}/like — Toggle like on an approved post."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.blogpost import BlogPostStatus
from app.models.user import User
from app.repositories.blogposts import get_blogpost_by_id, toggle_like
from .router import router


@router.post("/{post_id}/like")
async def like_blogpost(
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Toggle like on a blog post.

    - Requires authentication.
    - Only allowed on **approved** posts.
    - If already liked → unliked. If not liked → liked.

    Returns `{ "liked": bool, "likes_count": int }`.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post["status"] != BlogPostStatus.approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Likes are only allowed on approved posts",
        )

    return await toggle_like(db=db, blogpost_id=post_id, user_id=current_user.id)
