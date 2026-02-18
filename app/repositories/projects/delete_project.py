"""
Repository function for deleting a project.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.repositories.projects.get_project_by_id import get_project_by_id


async def delete_project(
    db: AsyncSession,
    project_id: UUID,
) -> None:
    """
    Delete a project from the database.
    
    Args:
        db: Database session
        project_id: UUID of the project to delete
    
    Raises:
        ValueError: If project not found
    """
    project = await get_project_by_id(db, project_id)
    
    if not project:
        raise ValueError("Project not found")
    
    await db.delete(project)
    await db.commit()
