from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class EventRegistrationRead(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventRegistrationWithEvent(BaseModel):
    id: UUID
    event_id: UUID
    registered_at: datetime
    event: "EventBrief"

    model_config = ConfigDict(from_attributes=True)


class EventBrief(BaseModel):
    id: UUID
    title: str
    date: str
    location: str | None = None

    model_config = ConfigDict(from_attributes=True)
