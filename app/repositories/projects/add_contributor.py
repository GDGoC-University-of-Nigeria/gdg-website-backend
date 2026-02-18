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
