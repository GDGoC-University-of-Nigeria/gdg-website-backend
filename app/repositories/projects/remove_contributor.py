

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from app.models.project_contributor import ProjectContributor


async def remove_contributor(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
) -> None:
    
    stmt = delete(ProjectContributor).where(
        ProjectContributor.project_id == project_id,
        ProjectContributor.user_id == user_id,
    )
    
    result = await db.execute(stmt)
    await db.commit()
    
    if result.rowcount == 0:
        raise ValueError("Contributor not found")
