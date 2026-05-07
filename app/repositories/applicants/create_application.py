from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applicant import Applicant


async def create_application(
    db: AsyncSession,
    user_id: UUID,
    project_id: UUID,
    role: str,
) -> Applicant:
    existing = await db.execute(
        select(Applicant).where(
            Applicant.user_id == user_id,
            Applicant.project_id == project_id,
        )
    )
    if existing.scalar_one_or_none():
        raise ValueError("You have already applied to this project")

    applicant = Applicant(user_id=user_id, project_id=project_id, role=role)
    db.add(applicant)
    await db.commit()
    await db.refresh(applicant)
    return applicant
