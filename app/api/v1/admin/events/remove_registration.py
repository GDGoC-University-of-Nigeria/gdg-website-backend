"""DELETE /api/v1/admin/events/{event_id}/registrations/{user_id} — Admin remove a user's registration."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.event_registrations import (
    delete_registration,
    get_registration_by_event_and_user,
)
from app.repositories.events.get_event_by_id import get_event_by_id
from .router import router


@router.delete(
    "/{event_id}/registrations/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def admin_remove_registration(
    event_id: UUID = Path(...),
    user_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Admin: remove a specific user's registration from an event.
    Useful for correcting duplicate or erroneous registrations.
    """
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    registration = await get_registration_by_event_and_user(db, event_id, user_id)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found for this user and event",
        )

    await delete_registration(db=db, registration=registration)
