"""
Speaker model for the GDGoC UNN API.

This module defines the Speaker model for managing guest speakers and presenters
at GDGoC UNN events.
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.sql import func
import uuid


class Speakers(Base):
    """
    Speaker model representing a guest speaker or presenter at an event.
    
    Speakers are individuals invited to present at GDGoC UNN events. They can be
    industry professionals, academics, or experienced developers who share their
    knowledge with the community.
    
    Attributes:
        id (UUID): Unique identifier for the speaker
        event_id (UUID): ID of the event where this speaker is presenting
        name (str): Speaker's full name
        image_url (str, optional): URL to speaker's profile photo
        bio (str): Speaker's biography and background
        content_format (str): Format of the bio content (default: "markdown")
        topic (str, optional): Specific topic the speaker will present
        niche (str): Speaker's area of expertise (e.g., "Cloud Computing", "Mobile Dev")
        added_at (datetime): Timestamp when the speaker was added to the event
    
    Relationships:
        event: Event where this speaker is presenting (to be implemented)
    
    Notes:
        - Multiple speakers can be associated with a single event
        - Bio supports markdown formatting for rich text
        - Niche helps attendees understand the speaker's expertise area
    """
    
    __tablename__ = "speakers"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event relationship
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)

    # Speaker information
    name = Column(String, nullable=False)  # Speaker's full name
    image_url = Column(String, nullable=True)  # Profile photo
    bio = Column(Text, nullable=False)  # Speaker biography
    content_format = Column(String, default="markdown")  # Bio format
    
    # Presentation details
    topic = Column(String, nullable=True)  # Presentation topic/title
    niche = Column(String, nullable=False)  # Area of expertise
    
    # Metadata
    added_at = Column(DateTime, server_default=func.now())  # Creation timestamp

    # Relationships (to be implemented)
    # event = relationship("Event", back_populates="speakers")
