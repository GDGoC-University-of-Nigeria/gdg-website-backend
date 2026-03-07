from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.speaker import Speakers
from app.schemas.speaker import SpeakerCreate


async def create_speaker(
    db: AsyncSession,
    event_id: UUID,
    payload: SpeakerCreate,
) -> Speakers:
    speaker = Speakers(
        event_id=event_id,
        name=payload.name,
        bio=payload.bio,
        image_url=payload.image_url,
        topic=payload.topic,
        niche=payload.niche,
    )
    db.add(speaker)
    await db.commit()
    await db.refresh(speaker)
    return speaker
