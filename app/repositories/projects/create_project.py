"""
Repository function for creating a new project.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.project import Project
from app.schemas.project import ProjectCreate


async def create_project(
    db: AsyncSession,
    payload: ProjectCreate,
    creator_id: UUID,
) -> Project:
    """
    Create a new project in the database.
    
    Args:
        db: Database session
        payload: Project creation data
        creator_id: UUID of the user creating the project
    
    Returns:
        Created project instance
    """
    project = Project(**payload.model_dump(), creator_id=creator_id)
    db.add(project)
    await db.commit()
    await db.refresh(project, attribute_names=["creator", "contributors"])
    return project
