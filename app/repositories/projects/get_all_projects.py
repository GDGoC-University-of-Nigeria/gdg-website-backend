

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.project import Project, ProjectType, ProjectStatus
from app.models.project_contributor import ProjectContributor
from app.models.user import User


async def get_all_projects(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    project_type: ProjectType | None = None,
    status: ProjectStatus | None = None,
) -> list[Project]:

    query = (
        select(Project)
        .options(
            selectinload(Project.creator).selectinload(User.profile),
            selectinload(Project.contributors).selectinload(ProjectContributor.user).selectinload(User.profile)
        )
        .offset(skip)
        .limit(limit)
    )
    
    if project_type:
        query = query.where(Project.project_type == project_type)
    if status:
        query = query.where(Project.status == status)
    
    result = await db.execute(query)
    return list(result.scalars().all())
