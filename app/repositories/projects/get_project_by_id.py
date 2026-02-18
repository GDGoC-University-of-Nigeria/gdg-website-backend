"""
Repository function for fetching a single project by ID.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.project import Project
from app.models.project_contributor import ProjectContributor


async def get_project_by_id(
    db: AsyncSession,
    project_id: UUID,
) -> Project | None:
    """
    Fetch a single project by its ID.
    
    Args:
        db: Database session
        project_id: UUID of the project to fetch
    
    Returns:
        Project instance if found, None otherwise
    """
    query = (
        select(Project)
        .where(Project.id == project_id)
        .options(
            selectinload(Project.creator),
            selectinload(Project.contributors).selectinload(ProjectContributor.user)
        )
    )
    
    result = await db.execute(query)
    return result.scalar_one_or_none()
