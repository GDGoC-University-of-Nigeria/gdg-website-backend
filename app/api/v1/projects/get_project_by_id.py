

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.project import ProjectDetailRead
from app.repositories.projects import get_project_by_id as get_project_by_id_repo
from .router import router


@router.get(
    "/{project_id}",
    response_model=ProjectDetailRead,
)
async def get_project_by_id_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch a single project by its ID.
    
    - Public endpoint (no authentication required)
    - Includes creator and contributors in the response
    - Returns 404 if project not found
    """
    project = await get_project_by_id_repo(db, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return project
