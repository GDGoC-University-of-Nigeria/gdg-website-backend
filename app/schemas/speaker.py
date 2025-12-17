"""
Speaker schemas for the GDGoC UNN API.

This module defines Pydantic schemas for managing speakers and presenters
at GDGoC UNN events.
"""

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class SpeakerBase(BaseModel):
    """
    Base schema with common speaker fields.
    
    Contains fields shared across speaker creation and reading operations.
    
    Attributes:
        event_id (UUID): ID of the event where the speaker is presenting
        name (str): Speaker's full name
        bio (str): Speaker's biography and background (supports markdown)
        image_url (str): URL to speaker's profile photo
        topic (str, optional): Specific topic the speaker will present
        niche (str): Speaker's area of expertise (e.g., "Cloud Computing")
    """
    event_id: UUID
    name: str
    bio: str
    image_url: str
    topic: Optional[str] = None
    niche: str


class SpeakerCreate(SpeakerBase):
    """
    Schema for adding a new speaker to an event.
    
    Inherits all fields from SpeakerBase. Used when event organizers
    add speakers to their events.
    
    Notes:
        - Multiple speakers can be added to a single event
        - Bio supports markdown formatting
    """
    pass  # All fields included in Base


class SpeakerRead(SpeakerBase):
    """
    Schema for reading speaker data from the API.
    
    Extends SpeakerBase with database-generated fields.
    
    Attributes:
        id (UUID): Unique speaker identifier
        added_at (datetime): Timestamp when the speaker was added
    """
    id: UUID
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SpeakerUpdate(BaseModel):
    """
    Schema for updating speaker information.
    
    All fields are optional to allow partial updates. Only provided fields
    will be updated in the database.
    
    Attributes:
        name (str, optional): Updated speaker name
        bio (str, optional): Updated biography
        image_url (str, optional): Updated profile photo URL
        topic (str, optional): Updated presentation topic
        niche (str, optional): Updated area of expertise
    """
    name: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    topic: Optional[str] = None
    niche: Optional[str] = None
