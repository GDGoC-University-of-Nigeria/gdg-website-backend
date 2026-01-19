from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.event import Event
from app.schemas.event import EventCreate


async def create_event(
    db: AsyncSession,
    payload: EventCreate,
    creator_id: UUID,
) -> Event:
    event = Event(**payload.model_dump(), creator_id=creator_id)
    db.add(event)
    await db.commit()
    await db.refresh(event, attribute_names=["speakers"])
    return event

