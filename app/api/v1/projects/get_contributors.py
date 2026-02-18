"""
Get project contributors endpoint.
"""

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.project import ProjectContributorRead
from app.repositories.projects import get_project_contributors as get_project_contributors_repo
from .router import router


@router.get(
    "/{project_id}/contributors",
    response_model=list[ProjectContributorRead],
)
async def get_contributors_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all contributors for a project.
    
    - Public endpoint (no authentication required)
    - Returns list of contributors with user details
    """
    return await get_project_contributors_repo(
        db=db,
        project_id=project_id,
    )
