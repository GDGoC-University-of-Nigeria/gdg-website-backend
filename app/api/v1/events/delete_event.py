from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.event import (
    EventCreate,
    EventResponse,
)
from app.repositories.events import delete_event as delete_event_repo, get_event_by_id
from app.dependencies.require_admin import require_admin
from app.models.user import User
from .router import router

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_endpoint(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    event = await get_event_by_id(db, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    await delete_event_repo(db, event)

    return {"message": "Event deleted successfully"}
