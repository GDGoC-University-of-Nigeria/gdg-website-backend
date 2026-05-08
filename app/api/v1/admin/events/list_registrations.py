"""GET /api/v1/admin/events/{event_id}/registrations — List all registrations for an event."""

from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.event_registrations import get_event_registrations
from app.repositories.events.get_event_by_id import get_event_by_id
from app.schemas.user import EventRegistrationRead
from .router import router


@router.get("/{event_id}/registrations", response_model=List[EventRegistrationRead])
async def admin_list_registrations(
    event_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    List all registrations for a given event.
    Returns registrant user info alongside registration metadata.
    """
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    return await get_event_registrations(db=db, event_id=event_id)
