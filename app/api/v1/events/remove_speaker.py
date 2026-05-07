"""DELETE /events/{event_id}/speakers/{speaker_id} — Remove a speaker (admin only)."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.speakers import delete_speaker
from .router import router


@router.delete(
    "/{event_id}/speakers/{speaker_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_speaker_endpoint(
    event_id: UUID = Path(..., description="Event ID"),
    speaker_id: UUID = Path(..., description="Speaker ID"),
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    """Remove a speaker from an event. Admin only."""
    deleted = await delete_speaker(db=db, event_id=event_id, speaker_id=speaker_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
