"""PATCH /api/v1/comments/{id} — Update own comment."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.comments import get_comment_by_id, update_comment
from app.schemas.comment import CommentRead, CommentUpdate
from .router import router


@router.patch("/{comment_id}", response_model=CommentRead)
async def edit_comment(
    payload: CommentUpdate,
    comment_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a comment's content.

    - Requires authentication.
    - Only the **author** can edit their own comment.
    """
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own comments",
        )

    return await update_comment(db=db, comment=comment, payload=payload)
