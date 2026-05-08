"""PATCH /api/v1/admin/users/{user_id}/role — Promote or demote a user."""

from uuid import UUID
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.users.get_user_by_id import get_user_by_id
from app.repositories.users.update_user_role import update_user_role
from app.schemas.user import UserResponse, UserRoleUpdate
from .router import router


@router.patch("/{user_id}/role", response_model=UserResponse)
async def admin_update_user_role(
    payload: UserRoleUpdate,
    user_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Update a user's admin role.
    
    - Admin privileges required.
    - An admin cannot demote themselves.
    """
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own admin role",
        )

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return await update_user_role(db=db, user=user, is_admin=payload.is_admin)
