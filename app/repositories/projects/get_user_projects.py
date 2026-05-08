"""Get all projects created by a specific user."""

from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.project_contributor import ProjectContributor
from app.models.user import User


async def get_user_projects(
    db: AsyncSession,
    user_id: UUID,
) -> Sequence[Project]:
    """Return all projects where creator_id == user_id, with contributors and creator eager-loaded."""
    stmt = (
        select(Project)
        .options(
            selectinload(Project.creator).selectinload(User.profile),
            selectinload(Project.contributors).selectinload(ProjectContributor.user).selectinload(User.profile),
        )
        .where(Project.creator_id == user_id)
        .order_by(Project.created_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()
