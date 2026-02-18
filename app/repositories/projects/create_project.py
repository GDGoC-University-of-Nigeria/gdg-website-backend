

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
    await db.refresh(project, attribute_names=["creator", "contributors"])
    return project
