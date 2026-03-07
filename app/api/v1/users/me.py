from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.get_current_user import get_current_user
from app.schemas.user import UserResponse, UpdateUserRequest
from app.repositories.users.update_user import update_user
from app.db.session import get_db

from .router import router


@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    payload: UpdateUserRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's profile (full_name, email, phone)."""
    try:
        updated = await update_user(
            db=db,
            user_id=user.id,
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
