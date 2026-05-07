from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.speaker import Speakers
from app.schemas.speaker import SpeakerUpdate


async def update_speaker(
    db: AsyncSession,
    event_id: UUID,
    speaker_id: UUID,
    payload: SpeakerUpdate,
) -> Speakers | None:
    result = await db.execute(
        select(Speakers).where(
            Speakers.id == speaker_id,
            Speakers.event_id == event_id,
        )
    )
    speaker = result.scalar_one_or_none()
    if not speaker:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(speaker, field, value)
    await db.commit()
    await db.refresh(speaker)
    return speaker
