"""PATCH /events/{event_id}/speakers/{speaker_id} — Update a speaker (admin only)."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.speakers import update_speaker
from app.schemas.speaker import SpeakerUpdate, SpeakerResponse
from .router import router


@router.patch(
    "/{event_id}/speakers/{speaker_id}",
    response_model=SpeakerResponse,
)
async def update_speaker_endpoint(
    payload: SpeakerUpdate,
    event_id: UUID = Path(..., description="Event ID"),
    speaker_id: UUID = Path(..., description="Speaker ID"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Update a speaker on an event. Admin only."""
    speaker = await update_speaker(db=db, event_id=event_id, speaker_id=speaker_id, payload=payload)
    if not speaker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
    return speaker
