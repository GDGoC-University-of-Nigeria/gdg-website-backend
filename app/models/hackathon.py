from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID

class HackathonRegistration(Base):
    __tablename__ = "hackathon_registrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True) # Optional for non-logged-in users
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    github_link = Column(String, nullable=True)
    team_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="hackathon_registrations")
