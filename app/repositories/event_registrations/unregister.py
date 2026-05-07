from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_registration import EventRegistration


async def unregister_from_event(
    db: AsyncSession,
    event_id: UUID,
    user_id: UUID,
) -> bool:
    result = await db.execute(
        select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id,
        )
    )
    reg = result.scalar_one_or_none()
    if not reg:
        return False
    await db.delete(reg)
    await db.commit()
    return True
