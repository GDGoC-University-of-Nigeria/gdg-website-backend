"""
BlogPost schemas for the GDGoC UNN API.

This module defines Pydantic schemas for blog post operations including
creating and reading blog posts written by community members.
"""

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class BlogPostCreate(BaseModel):
    """
    Schema for creating a new blog post.
    
    Community members can create blog posts about technical topics, tutorials,
    or project experiences. Posts require admin verification before being publicly visible.
    
    Attributes:
        title (str): Blog post title/headline
        image_url (str, optional): URL to featured/cover image
        content (str): Full blog post content (supports markdown)
        niche (str, optional): Topic category (e.g., "Web Development", "AI/ML")
    
    Notes:
        - Posts are created with is_verified=False by default
        - Content is expected to be in markdown format
        - author_id is set automatically from the authenticated user
    """
    title: str
    image_url: str | None = None
    content: str
    niche: str | None = None


class BlogPostRead(BlogPostCreate):
    """
    Schema for reading blog post data from the API.
    
    Extends BlogPostCreate with database-generated fields and verification status.
    
    Attributes:
        id (UUID): Unique blog post identifier
        author_id (UUID): ID of the user who wrote the post
        is_verified (bool): Whether the post has been approved by admins
    
    Notes:
        - Only verified posts should be shown to non-admin users
        - Authors can see their own unverified posts
    """
    id: UUID
    author_id: UUID
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)
