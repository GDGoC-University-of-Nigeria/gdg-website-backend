from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.event import Event
import uuid


class User(Base):
 
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=True)  
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False, server_default=text('false'), nullable=False)
    provider = Column(String, nullable=False)  # OAuth provider (e.g., "google")
    provider_user_id = Column(String, nullable=False)     
    created_at = Column(DateTime, default=func.now())  # Registration timestamp

    # Relationships (commented out until implemented)
    
    # projects = relationship("Project", back_populates="contributor")
    # blogposts = relationship("BlogPost", back_populates="author")
    # applications = relationship("Applicant", back_populates="user")
