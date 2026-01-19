from fastapi import Depends, APIRouter
from app.dependencies.get_current_user import get_current_user
from app.schemas.user import UserResponse

from .router import router

@router.get("/me", response_model=UserResponse)
async def get_me(user = Depends(get_current_user)):
    return user
