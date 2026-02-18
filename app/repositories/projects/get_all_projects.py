"""
Repository function for fetching all projects.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.project import Project, ProjectType
from app.models.project_contributor import ProjectContributor


async def get_all_projects(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    project_type: ProjectType | None = None,
) -> list[Project]:
    """
    Fetch all projects with pagination and optional filtering.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        project_type: Optional filter by project type
    
    Returns:
        List of projects with eager-loaded relationships
    """
    query = (
        select(Project)
        .options(
            selectinload(Project.creator),
            selectinload(Project.contributors).selectinload(ProjectContributor.user)
        )
        .offset(skip)
        .limit(limit)
    )
    
    if project_type:
        query = query.where(Project.project_type == project_type)
    
    result = await db.execute(query)
    return list(result.scalars().all())
