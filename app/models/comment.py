"""Comment model for blog posts."""

import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Index, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    blogpost_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blogposts.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_hidden = Column(Boolean, nullable=False, default=False, server_default="false")

    # Relationships
    user = relationship("User", back_populates="comments")
    blogpost = relationship("BlogPost", back_populates="comments")

    __table_args__ = (
        Index("ix_comments_blogpost_id", "blogpost_id"),
        Index("ix_comments_user_id", "user_id"),
    )
