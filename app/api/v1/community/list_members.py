"""GET /api/v1/community/members - List non-admin community members (paginated)."""

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.users.get_community_members import get_community_members
from app.schemas.user import UserResponse
from .router import router


@router.get("/members", response_model=list[UserResponse])
async def list_community_members(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List non-admin community members. Available to any authenticated user.
    Paginated via skip and limit.
    """
    return await get_community_members(db=db, skip=skip, limit=limit)
