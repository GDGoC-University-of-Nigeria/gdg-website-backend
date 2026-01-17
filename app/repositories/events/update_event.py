from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.event import Event
from app.schemas.event import EventUpdate


async def update_event(
    db: AsyncSession,
    event: Event,
    payload: EventUpdate,
) -> Event:
    # Only update fields that are not None
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(event, key, value)

    await db.commit()
    await db.refresh(event, attribute_names=["speakers"])
    return event
