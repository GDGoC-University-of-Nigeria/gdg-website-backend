"""DELETE /events/{event_id}/register — Unregister from an event."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.event_registrations import unregister_from_event
from .router import router


@router.delete(
    "/{event_id}/register",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unregister_endpoint(
    event_id: UUID = Path(..., description="Event ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Unregister the current user from an event."""
    removed = await unregister_from_event(db=db, event_id=event_id, user_id=current_user.id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
