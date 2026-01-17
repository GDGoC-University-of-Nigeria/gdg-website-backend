from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime
from uuid import UUID
from typing import Optional, List
from app.schemas.speaker import SpeakerResponse


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    start_time: time
    end_time: time
    image_url: Optional[str] = None
    location: Optional[str] = None


class EventCreate(EventBase):
    
    pass


class EventResponse(EventBase):
    id: UUID
    attendees: Optional[int] = None
    speakers: List[SpeakerResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
