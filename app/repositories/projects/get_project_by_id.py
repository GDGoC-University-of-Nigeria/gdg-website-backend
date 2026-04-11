

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.project import Project
from app.models.project_contributor import ProjectContributor
from app.models.user import User


async def get_project_by_id(
    db: AsyncSession,
    project_id: UUID,
) -> Project | None:

    query = (
        select(Project)
        .where(Project.id == project_id)
        .options(
            selectinload(Project.creator).selectinload(User.profile),
            selectinload(Project.contributors).selectinload(ProjectContributor.user).selectinload(User.profile)
        )

    )
    
    result = await db.execute(query)
    return result.scalar_one_or_none()
