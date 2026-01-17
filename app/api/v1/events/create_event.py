from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_db
from app.schemas.event import (
    EventCreate,
    EventResponse,
)
from app.repositories.events import create_event as create_event_repo
from app.dependencies.require_admin import require_admin
from app.models.user import User
from .router import router

@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event_endpoint(
    payload: EventCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return await create_event_repo(
        db=db,
        payload=payload,
        creator_id=admin.id,
    )
