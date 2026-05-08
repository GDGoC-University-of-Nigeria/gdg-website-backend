"""GET /api/v1/users/me/projects — List the current user's created projects."""

from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.projects import get_user_projects
from app.schemas.project import ProjectDetailRead
from .router import router


@router.get("/me/projects", response_model=List[ProjectDetailRead])
async def list_my_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all projects created by the authenticated user.
    Includes contributors for each project.
    """
    return await get_user_projects(db=db, user_id=current_user.id)
