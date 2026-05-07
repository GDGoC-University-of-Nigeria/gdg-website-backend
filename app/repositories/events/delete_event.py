from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event


async def delete_event(db: AsyncSession, event: Event) -> None:
    await db.delete(event)
    await db.commit()
