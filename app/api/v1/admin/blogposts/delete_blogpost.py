"""DELETE /api/v1/admin/blogposts/{post_id} — Admin takedown."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.blogposts import delete_blogpost, get_blogpost_by_id
from .router import router


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_blogpost(
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Admin takedown — permanently delete any blog post regardless of status.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    await delete_blogpost(db=db, post=post)
