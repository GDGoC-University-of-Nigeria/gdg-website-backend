"""Publish an event (one-way admin action)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event


async def publish_event(db: AsyncSession, event: Event) -> Event:
    """Mark an event as published. This is a one-way, irreversible transition."""
    event.is_published = True
    await db.commit()
    await db.refresh(event)
    return event
