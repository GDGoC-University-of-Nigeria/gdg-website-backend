"""
Repository function for adding a contributor to a project.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from app.models.project_contributor import ProjectContributor


async def add_contributor(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
    role: str,
) -> ProjectContributor:
    """
    Add a user as a contributor to a project.
    
    Args:
        db: Database session
        project_id: UUID of the project
        user_id: UUID of the user to add
        role: Contributor's role in the project
    
    Returns:
        Created contributor instance
    
    Raises:
        IntegrityError: If user is already a contributor (duplicate)
    """
    contributor = ProjectContributor(
        project_id=project_id,
        user_id=user_id,
        role=role,
    )
    
    db.add(contributor)
    
    try:
        await db.commit()
        await db.refresh(contributor, attribute_names=["user"])
        return contributor
    except IntegrityError:
        await db.rollback()
        raise ValueError("User is already a contributor to this project")
