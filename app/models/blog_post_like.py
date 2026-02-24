"""BlogPostLike model — one like per user per post, enforced via composite PK."""

import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, Index

from app.db.base import Base


class BlogPostLike(Base):
    __tablename__ = "blog_post_likes"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    blogpost_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blogposts.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="likes")
    blogpost = relationship("BlogPost", back_populates="likes")

    __table_args__ = (
        Index("ix_blog_post_likes_blogpost_id", "blogpost_id"),
    )
