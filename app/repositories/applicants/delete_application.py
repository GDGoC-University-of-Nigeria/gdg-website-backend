"""Withdraw (delete) a pending project application."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applicant import Applicant


async def delete_application(db: AsyncSession, application: Applicant) -> None:
    """Permanently delete a project application."""
    await db.delete(application)
    await db.commit()
