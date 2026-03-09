from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.applicant import Applicant


async def get_project_applications(
    db: AsyncSession,
    project_id: UUID,
) -> Sequence[Applicant]:
    result = await db.execute(
        select(Applicant)
        .where(Applicant.project_id == project_id)
        .options(selectinload(Applicant.user))
        .order_by(Applicant.applied_at.desc())
    )
    return result.scalars().all()


async def get_user_applications(
    db: AsyncSession,
    user_id: UUID,
) -> Sequence[Applicant]:
    result = await db.execute(
        select(Applicant)
        .where(Applicant.user_id == user_id)
        .options(selectinload(Applicant.project))
        .order_by(Applicant.applied_at.desc())
    )
    return result.scalars().all()
