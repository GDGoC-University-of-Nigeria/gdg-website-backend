from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.event import (
    EventResponse,
)
from app.repositories.events import get_event_by_id as get_event_by_id_repo
from .router import router

@router.get(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
)
async def get_event_by_id_endpoint(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    
):
    event = await get_event_by_id_repo(db, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
