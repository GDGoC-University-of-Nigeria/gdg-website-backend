from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.event_registration import EventRegistration


async def register_for_event(
    db: AsyncSession,
    event_id: UUID,
    user_id: UUID,
) -> EventRegistration:
    reg = EventRegistration(event_id=event_id, user_id=user_id)
    db.add(reg)
    try:
        await db.commit()
        await db.refresh(reg)
        return reg
    except IntegrityError:
        await db.rollback()
        raise ValueError("Already registered for this event")
