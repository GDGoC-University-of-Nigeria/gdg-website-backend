"""
Event model for the GDGoC UNN API.

This module defines the Event model representing community events such as workshops,
meetups, hackathons, and tech talks organized by GDGoC UNN.
"""

from sqlalchemy import Column, Integer, String, Time, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.sql import func
import uuid


class Event(Base):
    """
    Event model representing a GDGoC UNN community event.
    
    Events are activities organized by the community, including workshops, meetups,
    hackathons, study sessions, and guest speaker sessions. Each event has details
    about timing, location, and associated speakers.
    
    Attributes:
        id (UUID): Unique identifier for the event
        title (str): Event name/title
        description (str, optional): Detailed description of the event
        image_url (str, optional): URL to event banner/poster image
        date (date): Date when the event takes place
        start_time (time): Event start time
        end_time (time): Event end time
        location (str, optional): Event venue (physical or virtual link)
        creator_id (int): ID of the user who created the event
        created_at (datetime): Timestamp when the event was created
    
    Relationships:
        creator: User who created this event (to be implemented)
        speakers: Speakers presenting at this event (to be implemented)
        attendees: Users registered for this event (to be implemented)
    """
    
    __tablename__ = "events"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    # Event details
    title = Column(String, index=True)  # Event name (indexed for search)
    description = Column(String, nullable=True)  # Full event description
    image_url = Column(String, nullable=True)  # Event banner/poster
    
    # Scheduling information
    date = Column(Date, nullable=False)  # Event date
    start_time = Column(Time, nullable=False)  # Start time
    end_time = Column(Time, nullable=False)  # End time
    
    # Location and creator
    location = Column(String, nullable=True)  # Venue or virtual meeting link
    creator_id = Column(Integer, ForeignKey("users.id"))  # Event organizer
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())  # Creation timestamp

    # Relationships (to be implemented)
    # creator = relationship("User", back_populates="events")
    # speakers = relationship("Speaker", back_populates="event")
    # attendees = relationship("EventAttendee", back_populates="event")