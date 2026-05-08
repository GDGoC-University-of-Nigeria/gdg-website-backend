"""PATCH /api/v1/admin/users/{user_id}/reactivate — Reactivate a deactivated user."""

from uuid import UUID
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.users.get_user_by_id import get_user_by_id
from app.repositories.users.reactivate_user import reactivate_user
from app.schemas.user import UserResponse
from .router import router


@router.patch("/{user_id}/reactivate", response_model=UserResponse)
async def admin_reactivate_user(
    user_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Reactivate a previously deactivated user account.
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is already active",
        )

    return await reactivate_user(db=db, user=user)
