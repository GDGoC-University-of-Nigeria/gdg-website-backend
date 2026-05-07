"""GET /events/{event_id}/registration — Check registration status."""

from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.event_registrations import is_registered
from .router import router


@router.get("/{event_id}/registration")
async def registration_status_endpoint(
    event_id: UUID = Path(..., description="Event ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if the current user is registered for an event."""
    registered = await is_registered(db=db, event_id=event_id, user_id=current_user.id)
    return {"registered": registered}
