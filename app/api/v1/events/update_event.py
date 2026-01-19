from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.event import (
    EventUpdate,
    EventResponse,
)
from app.repositories.events import update_event as update_event_repo, get_event_by_id
from app.dependencies.require_admin import require_admin
from app.models.user import User
from .router import router

@router.put("/{event_id}", response_model=EventResponse)
async def update_event_endpoint(
    event_id: UUID,
    payload: EventUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    event = await get_event_by_id(db, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return await update_event_repo(db, event, payload)
