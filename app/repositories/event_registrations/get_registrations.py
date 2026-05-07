from uuid import UUID
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event_registration import EventRegistration


async def get_event_registrations(
    db: AsyncSession,
    event_id: UUID,
) -> Sequence[EventRegistration]:
    result = await db.execute(
        select(EventRegistration)
        .where(EventRegistration.event_id == event_id)
        .options(selectinload(EventRegistration.user))
        .order_by(EventRegistration.registered_at.desc())
    )
    return result.scalars().all()


async def get_user_registrations(
    db: AsyncSession,
    user_id: UUID,
) -> Sequence[EventRegistration]:
    result = await db.execute(
        select(EventRegistration)
        .where(EventRegistration.user_id == user_id)
        .options(selectinload(EventRegistration.event))
        .order_by(EventRegistration.registered_at.desc())
    )
    return result.scalars().all()


async def is_registered(
    db: AsyncSession,
    event_id: UUID,
    user_id: UUID,
) -> bool:
    result = await db.execute(
        select(func.count()).select_from(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id,
        )
    )
    return result.scalar_one() > 0
