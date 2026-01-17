from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.event import (
    EventResponse,
)
from app.repositories.events import get_all_events
from .router import router

@router.get(
    "/",
    response_model=list[EventResponse], 
    status_code=status.HTTP_200_OK,
)
async def list_events(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_events(
        db=db,
    )
