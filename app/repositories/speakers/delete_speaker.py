from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.speaker import Speakers


async def delete_speaker(
    db: AsyncSession,
    event_id: UUID,
    speaker_id: UUID,
) -> bool:
    result = await db.execute(
        select(Speakers).where(
            Speakers.id == speaker_id,
            Speakers.event_id == event_id,
        )
    )
    speaker = result.scalar_one_or_none()
    if not speaker:
        return False
    db.delete(speaker)
    await db.commit()
    return True
