"""
Delete project endpoint.
"""

from fastapi import Depends, Path, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.repositories.projects import delete_project as delete_project_repo
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from .router import router


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """
    Delete a project.
    
    - **Personal projects**: Only the creator can delete
    - **Community projects**: Only admins can delete
    
    Deleting a project will also cascade delete all contributors.
    """
    current_user, project = auth_data
    
    await delete_project_repo(db=db, project_id=project_id)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
