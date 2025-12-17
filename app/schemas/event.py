"""
Event schemas for the GDGoC UNN API.

This module defines Pydantic schemas for event-related operations including
creating, reading, and updating events.
"""

from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime
from uuid import UUID
from typing import Optional


class EventBase(BaseModel):
    """
    Base schema with common event fields.
    
    This base class contains fields shared across event creation and reading operations.
    
    Attributes:
        title (str): Event name/title
        description (str): Detailed event description
        date (date): Event date
        start_time (time): Event start time
        image_url (str): URL to event banner/poster
        end_time (time): Event end time
        location (str, optional): Event venue or virtual meeting link
    """
    title: str
    description: str
    date: date
    start_time: time
    image_url: str
    end_time: time
    location: str | None


class EventCreate(EventBase):
    """
    Schema for creating a new event.
    
    Extends EventBase with the creator_id field to track who created the event.
    
    Attributes:
        creator_id (UUID): ID of the user creating the event
    """
    creator_id: UUID


class EventRead(EventBase):
    """
    Schema for reading event data from the API.
    
    Extends EventBase with database-generated fields like id and created_at.
    
    Attributes:
        id (UUID): Unique event identifier
        created_at (datetime): Timestamp when the event was created
    """
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventUpdate(BaseModel):
    """
    Schema for updating an existing event.
    
    All fields are optional to allow partial updates. Only provided fields
    will be updated in the database.
    
    Attributes:
        title (str, optional): Updated event title
        description (str, optional): Updated event description
        date (date, optional): Updated event date
        start_time (time, optional): Updated start time
        end_time (time, optional): Updated end time
        location (str, optional): Updated event location
    """
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
