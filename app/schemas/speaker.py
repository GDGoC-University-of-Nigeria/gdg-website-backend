from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class SpeakerBase(BaseModel):
    
    name: str
    bio: str
    image_url: str
    topic: Optional[str] = None
    niche: str

class SpeakerCreate(SpeakerBase):
    
    pass

class SpeakerUpdate(BaseModel):
    
    name: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    topic: Optional[str] = None
    niche: Optional[str] = None

class SpeakerResponse(SpeakerBase):
    id: UUID
    event_id: UUID
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)
