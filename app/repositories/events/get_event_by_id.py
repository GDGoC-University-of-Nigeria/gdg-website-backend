from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.event import Event


async def get_event_by_id(db: AsyncSession, event_id: UUID) -> Event | None:
    result = await db.execute(
        select(Event)
        .options(selectinload(Event.speakers))
        .where(Event.id == event_id)
    )
    return result.scalars().first()

