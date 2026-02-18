

from fastapi import Depends, HTTPException, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.repositories.projects import remove_contributor as remove_contributor_repo
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from .router import router


@router.delete(
    "/{project_id}/contributors/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_contributor_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    user_id: UUID = Path(..., description="User ID of the contributor to remove"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """
    Remove a contributor from a project.
    
    - Only the project creator/owner can remove contributors
    - Returns 404 if the contributor is not found
    """
    current_user, project = auth_data
    
    try:
        await remove_contributor_repo(
            db=db,
            project_id=project_id,
            user_id=user_id,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
