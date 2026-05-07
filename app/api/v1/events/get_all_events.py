from datetime import date

from fastapi import Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.event import EventResponse
from app.repositories.events import get_all_events
from .router import router


@router.get(
    "/",
    response_model=list[EventResponse],
    status_code=status.HTTP_200_OK,
)
async def list_events(
    db: AsyncSession = Depends(get_db),
    from_date: date | None = Query(None, description="Filter events on or after this date"),
    limit: int = Query(100, ge=1, le=500, description="Maximum events to return"),
):
    return await get_all_events(db=db, from_date=from_date, limit=limit)
