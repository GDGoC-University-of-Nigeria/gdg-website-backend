
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.project import ProjectDetailRead, ProjectType, ProjectStatus
from app.repositories.projects import get_all_projects as get_all_projects_repo
from .router import router


@router.get(
    "/",
    response_model=list[ProjectDetailRead],
)
async def get_all_projects_endpoint(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum records to return"),
    project_type: ProjectType | None = Query(None, description="Filter by project type"),
    status: ProjectStatus | None = Query(None, description="Filter by status (ongoing/completed)"),
):
    """
    Fetch all projects with optional filtering and pagination.
    
    - Public endpoint (no authentication required)
    - Supports filtering by project type (personal/community) and status (ongoing/completed)
    - Includes creator and contributors in the response
    """
    return await get_all_projects_repo(
        db=db,
        skip=skip,
        limit=limit,
        project_type=project_type,
        status=status,
    )
