from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.repositories.users.soft_delete_user import soft_delete_user
from app.repositories.users.get_user_by_id import get_user_by_id
from app.models.user import User

from .router import router


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.is_active:
        return {"message": "User already deactivated"}

    await soft_delete_user(db, user_id)
    return {"message": "User deactivated"}

