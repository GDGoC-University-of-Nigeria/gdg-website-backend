from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.event import Event

async def get_all_events(db: AsyncSession) -> list[Event]:
    result = await db.execute(
        select(Event).options(selectinload(Event.speakers))
    )
    return result.scalars().all()
