from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func, text
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.event import Event
from app.models.event_registration import EventRegistration
import uuid
# from app.models.user_profile import UserProfile


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    provider = Column(String, nullable=False)             # "google"
    provider_user_id = Column(String, nullable=True)      # Google sub ID
    is_admin = Column(Boolean, default=False, server_default=text('false'), nullable=False)
    is_active = Column(Boolean, default=True, server_default=text('true'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    created_projects = relationship("Project", back_populates="creator", foreign_keys="Project.creator_id")
    contributed_projects = relationship("ProjectContributor", back_populates="user", cascade="all, delete-orphan")
    blogposts = relationship("BlogPost", back_populates="author", foreign_keys="BlogPost.author_id")
    approved_blogposts = relationship("BlogPost", back_populates="approver", foreign_keys="BlogPost.approved_by")
    applications = relationship("Applicant", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("BlogPostLike", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    event_registrations = relationship("EventRegistration", back_populates="user", cascade="all, delete-orphan")