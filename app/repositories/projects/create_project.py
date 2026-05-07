

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.project import Project
from app.schemas.project import ProjectCreate


async def create_project(
    db: AsyncSession,
    payload: ProjectCreate,
    creator_id: UUID,
) -> Project:
 
    project = Project(**payload.model_dump(), creator_id=creator_id)
    db.add(project)
    await db.commit()
    
    from app.repositories.projects.get_project_by_id import get_project_by_id
    # Re-fetch with all necessary options for the response
    return await get_project_by_id(db, project.id)
