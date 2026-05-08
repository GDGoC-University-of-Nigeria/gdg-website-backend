"""PATCH /api/v1/admin/events/{event_id}/publish — Admin publish an event (one-way)."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.events.get_event_by_id import get_event_by_id
from app.repositories.events.publish_event import publish_event
from app.schemas.event import EventResponse
from .router import router


@router.patch("/{event_id}/publish", response_model=EventResponse)
async def admin_publish_event(
    event_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Publish an event, making it publicly visible.

    This is a **one-way** transition. Once published, an event can only
    be removed by deleting it entirely — it cannot be unpublished.
    """
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    if event.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is already published",
        )

    return await publish_event(db=db, event=event)
