"""
Update project endpoint.
"""

from fastapi import Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.project import ProjectUpdate, ProjectDetailRead
from app.repositories.projects import update_project as update_project_repo
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from .router import router


@router.patch(
    "/{project_id}",
    response_model=ProjectDetailRead,
)
async def update_project_endpoint(
    payload: ProjectUpdate,
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """
    Update an existing project.
    
    - **Personal projects**: Only the creator can update
    - **Community projects**: Only admins can update
    
    All fields are optional - only provided fields will be updated.
    Note: project_type and creator_id cannot be changed.
    """
    current_user, project = auth_data
    
    return await update_project_repo(
        db=db,
        project_id=project_id,
        payload=payload,
    )
