"""GET /events/me/registrations — Get events the current user registered for."""

from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.event_registrations import get_user_registrations
from app.schemas.event_registration import EventRegistrationRead
from .router import router


@router.get("/me/registrations", response_model=List[EventRegistrationRead])
async def my_registrations_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all events the current user is registered for."""
    return await get_user_registrations(db=db, user_id=current_user.id)
