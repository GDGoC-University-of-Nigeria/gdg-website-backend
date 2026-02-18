

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.project_contributor import ProjectContributor


async def get_project_contributors(
    db: AsyncSession,
    project_id: UUID,
) -> list[ProjectContributor]:

    query = (
        select(ProjectContributor)
        .where(ProjectContributor.project_id == project_id)
        .options(selectinload(ProjectContributor.user))
    )
    
    result = await db.execute(query)
    return list(result.scalars().all())
