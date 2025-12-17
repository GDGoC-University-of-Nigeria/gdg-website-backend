"""
BlogPost model for the GDGoC UNN API.

This module defines the BlogPost model for managing blog posts written by
community members, covering technical topics, tutorials, and experiences.
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.sql import func
import uuid


class BlogPost(Base):
    """
    BlogPost model representing a blog article written by a community member.
    
    Community members can write and publish blog posts about technical topics,
    tutorials, project experiences, or other relevant content. Posts require
    verification by admins before being publicly visible.
    
    Attributes:
        id (UUID): Unique identifier for the blog post
        author_id (UUID): ID of the user who wrote the post
        title (str): Blog post title/headline
        image_url (str, optional): URL to featured/cover image
        content (str): Full blog post content
        content_format (str): Format of the content (default: "markdown")
        is_verified (bool): Whether the post has been approved by admins
        niche (str, optional): Topic category (e.g., "Web Development", "AI/ML", "DevOps")
        posted_at (datetime): Timestamp when the post was created
    
    Relationships:
        author: User who wrote this blog post (to be implemented)
    
    Notes:
        - Posts are created with is_verified=False and require admin approval
        - Content is stored in markdown format by default for rich formatting
        - The niche field helps categorize posts for easier discovery
    """
    
    __tablename__ = "blogposts"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Author relationship
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Post content
    title = Column(String, nullable=False)  # Post title
    image_url = Column(String, nullable=True)  # Featured image
    content = Column(Text, nullable=False)  # Full post content
    content_format = Column(String, default="markdown")  # Content format (markdown, html, etc.)

    # Moderation and categorization
    is_verified = Column(Boolean, default=False)  # Admin approval status
    niche = Column(String, nullable=True)  # Topic category/tag
    
    # Metadata
    posted_at = Column(DateTime, server_default=func.now())  # Publication timestamp

    # Relationships (to be implemented)
    # author = relationship("User", back_populates="blogposts")
