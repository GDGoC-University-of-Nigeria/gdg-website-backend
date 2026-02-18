"""
Add contributor to project endpoint.
"""

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db.session import get_db
from app.schemas.project import ProjectContributorCreate, ProjectContributorRead
from app.repositories.projects import add_contributor as add_contributor_repo
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from .router import router


@router.post(
    "/{project_id}/contributors",
    response_model=ProjectContributorRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_contributor_endpoint(
    payload: ProjectContributorCreate,
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """
    Add a contributor to a project.
    
    - Only the project creator/owner can add contributors
    - The user being added must exist in the database
    - Duplicate contributors will return a 400 error
    """
    current_user, project = auth_data
    
    # Verify the user exists
    user_result = await db.execute(
        select(User).where(User.id == payload.user_id)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    try:
        contributor = await add_contributor_repo(
            db=db,
            project_id=project_id,
            user_id=payload.user_id,
            role=payload.role,
        )
        return contributor
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
