"""
BlogPost model for the GDGoC UNN API.

Supports a moderated publishing workflow:
  - Community members submit posts (status = pending)
  - Admins approve or reject submissions
  - Only approved posts are publicly visible
"""

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class BlogPostStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class BlogPost(Base):

    __tablename__ = "blogposts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Author
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Content
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    content_format = Column(String, default="markdown")
    niche = Column(String, nullable=True)

    # Moderation
    status = Column(
        Enum(BlogPostStatus, name="blogpoststatus"),
        nullable=False,
        default=BlogPostStatus.pending,
        server_default="pending",
    )
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(String, nullable=True)

    # Timestamps
    posted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    author = relationship("User", back_populates="blogposts", foreign_keys=[author_id])
    approver = relationship("User", back_populates="approved_blogposts", foreign_keys=[approved_by])

    __table_args__ = (
        Index("ix_blogposts_status", "status"),
    )
