"""POST /events/{event_id}/speakers — Add a speaker to an event (admin only)."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.events import get_event_by_id
from app.repositories.speakers import create_speaker
from app.schemas.speaker import SpeakerCreate, SpeakerResponse
from .router import router


@router.post(
    "/{event_id}/speakers",
    response_model=SpeakerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_speaker_endpoint(
    payload: SpeakerCreate,
    event_id: UUID = Path(..., description="Event ID"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Add a speaker to an event. Admin only."""
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return await create_speaker(db=db, event_id=event_id, payload=payload)
