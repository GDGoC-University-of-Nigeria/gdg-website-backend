from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event import Event


async def get_all_events(
    db: AsyncSession,
    from_date: date | None = None,
    limit: int = 100,
) -> list[Event]:
    query = (
        select(Event)
        .options(selectinload(Event.speakers))
        .where(Event.is_published.is_(True))
        .order_by(Event.date.asc())
        .limit(limit)
    )
    if from_date is not None:
        query = query.where(Event.date >= from_date)
    result = await db.execute(query)
    return list(result.scalars().all())
