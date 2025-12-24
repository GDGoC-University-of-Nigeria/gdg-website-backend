from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db_session, get_current_active_user
from app.schemas.user import CompleteProfileRequest, UserRead
from app.models.user import User
from app.crud import user as crud_user

router = APIRouter()

@router.post("/complete-profile", response_model=UserRead)
async def complete_profile(
    profile_in: CompleteProfileRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    Complete user profile.
    """
    if current_user.profile_complete:
        raise HTTPException(status_code=400, detail="Profile already completed")
        
    # Update user
    updated_user = await crud_user.update(db, db_obj=current_user, obj_in=profile_in)
    
    # Mark as complete (if not already handled by update logic, but explicit here for safety)
    if not updated_user.profile_complete:
        updated_user.profile_complete = True
        db.add(updated_user)
        await db.commit()
        await db.refresh(updated_user)
        
    return updated_user

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
