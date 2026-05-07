"""POST /events/{event_id}/register — Register for an event."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.events import get_event_by_id
from app.repositories.event_registrations import register_for_event
from app.schemas.event_registration import EventRegistrationRead
from .router import router


@router.post(
    "/{event_id}/register",
    response_model=EventRegistrationRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_endpoint(
    event_id: UUID = Path(..., description="Event ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register the current user for an event."""
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    try:
        return await register_for_event(db=db, event_id=event_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
