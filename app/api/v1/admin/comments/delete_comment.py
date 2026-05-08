"""DELETE /api/v1/admin/comments/{comment_id} — Admin moderate (hard delete)."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.comments import delete_comment, get_comment_by_id
from .router import router


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_comment(
    comment_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Admin hard-delete a comment.
    Use this to permanently remove harmful or spam content.
    """
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    await delete_comment(db=db, comment=comment)
