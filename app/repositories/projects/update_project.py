

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.project import Project
from app.schemas.project import ProjectUpdate


async def update_project(
    db: AsyncSession,
    project_id: UUID,
    payload: ProjectUpdate,
) -> Project:
   
    from app.repositories.projects.get_project_by_id import get_project_by_id
    
    project = await get_project_by_id(db, project_id)
    
    if not project:
        raise ValueError("Project not found")
    
    # Update only provided fields
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    await db.commit()
    await db.refresh(project, attribute_names=["creator", "contributors"])
    return project
