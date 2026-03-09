from sqlalchemy import Column, Integer, String, Time, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.sql import func
from app.models.speaker import Speakers
import uuid


class Event(Base):

    __tablename__ = "events"

  
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    attendees = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    
    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    speakers = relationship("Speakers", back_populates="event", cascade="all, delete-orphan")
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")

