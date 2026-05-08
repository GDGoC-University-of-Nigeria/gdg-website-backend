"""Fetch a single project application by ID."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applicant import Applicant


async def get_application_by_id(
    db: AsyncSession,
    application_id: UUID,
) -> Applicant | None:
    """Return the Applicant row or None if not found."""
    result = await db.execute(
        select(Applicant).where(Applicant.id == application_id)
    )
    return result.scalar_one_or_none()
