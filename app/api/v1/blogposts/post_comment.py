"""POST /api/v1/blogposts/{id}/comments — Add a comment to an approved post."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.blogpost import BlogPostStatus
from app.models.user import User
from app.repositories.blogposts import get_blogpost_by_id
from app.repositories.comments import create_comment
from app.schemas.comment import CommentCreate, CommentRead
from .router import router


@router.post("/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def add_comment(
    payload: CommentCreate,
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a comment to a blog post.

    - Requires authentication.
    - Only allowed on **approved** posts.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post.status != BlogPostStatus.approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Comments are only allowed on approved posts",
        )

    return await create_comment(
        db=db,
        blogpost_id=post_id,
        user_id=current_user.id,
        payload=payload,
    )
