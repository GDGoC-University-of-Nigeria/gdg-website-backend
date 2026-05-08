"""Remove an event registration (admin moderation)."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_registration import EventRegistration


async def get_registration_by_event_and_user(
    db: AsyncSession,
    event_id: UUID,
    user_id: UUID,
) -> EventRegistration | None:
    """Fetch a registration by event + user composite key."""
    result = await db.execute(
        select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def delete_registration(
    db: AsyncSession,
    registration: EventRegistration,
) -> None:
    """Permanently delete a registration record."""
    await db.delete(registration)
    await db.commit()
