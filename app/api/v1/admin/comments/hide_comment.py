"""PATCH /api/v1/admin/comments/{comment_id}/hide — Admin hide/unhide a comment."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.comments import get_comment_by_id
from app.schemas.comment import CommentHide, CommentRead
from .router import router


@router.patch("/{comment_id}/hide", response_model=CommentRead)
async def admin_hide_comment(
    payload: CommentHide,
    comment_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Soft-hide or un-hide a comment.

    Hidden comments remain in the database but are excluded from
    the public comments listing. Useful for moderating content
    without permanent deletion.
    """
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    comment.is_hidden = payload.is_hidden
    await db.commit()
    await db.refresh(comment)
    return comment
