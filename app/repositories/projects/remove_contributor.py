"""
Repository function for removing a contributor from a project.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from app.models.project_contributor import ProjectContributor


async def remove_contributor(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
) -> None:
    """
    Remove a contributor from a project.
    
    Args:
        db: Database session
        project_id: UUID of the project
        user_id: UUID of the user to remove
    
    Raises:
        ValueError: If contributor not found
    """
    stmt = delete(ProjectContributor).where(
        ProjectContributor.project_id == project_id,
        ProjectContributor.user_id == user_id,
    )
    
    result = await db.execute(stmt)
    await db.commit()
    
    if result.rowcount == 0:
        raise ValueError("Contributor not found")
