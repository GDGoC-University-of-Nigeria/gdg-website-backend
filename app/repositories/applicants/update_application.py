from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applicant import Applicant
from app.models.project_contributor import ProjectContributor


async def approve_application(
    db: AsyncSession,
    applicant_id: UUID,
) -> Applicant | None:
    result = await db.execute(
        select(Applicant).where(Applicant.id == applicant_id)
    )
    applicant = result.scalar_one_or_none()
    if not applicant:
        return None

    applicant.is_contributor = True

    contributor = ProjectContributor(
        project_id=applicant.project_id,
        user_id=applicant.user_id,
        role=applicant.role,
    )
    db.add(contributor)

    await db.commit()
    await db.refresh(applicant)
    return applicant


async def reject_application(
    db: AsyncSession,
    applicant_id: UUID,
) -> bool:
    result = await db.execute(
        select(Applicant).where(Applicant.id == applicant_id)
    )
    applicant = result.scalar_one_or_none()
    if not applicant:
        return False
    await db.delete(applicant)
    await db.commit()
    return True
