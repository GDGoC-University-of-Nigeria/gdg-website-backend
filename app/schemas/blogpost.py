"""
BlogPost schemas for the GDGoC UNN API.

Supports a moderated publishing workflow:
  - Community members submit posts (status = pending)
  - Admins approve or reject submissions
  - Only approved posts are publicly visible
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BlogPostStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class BlogPostCreate(BaseModel):
    """Payload for submitting a new blog post (community members)."""
    title: str
    content: str
    image_url: str | None = None
    niche: str | None = None


class BlogPostUpdate(BaseModel):
    """Partial update — only allowed while status is pending."""
    title: str | None = None
    content: str | None = None
    image_url: str | None = None
    niche: str | None = None


class BlogPostReject(BaseModel):
    """Admin rejection payload."""
    rejection_reason: str | None = None


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class BlogPostRead(BaseModel):
    """Public-facing blog post response (approved posts only)."""
    id: UUID
    author_id: UUID
    title: str
    content: str
    image_url: str | None
    niche: str | None
    content_format: str | None
    status: BlogPostStatus
    posted_at: datetime | None
    updated_at: datetime | None
    approved_at: datetime | None
    # Engagement counts (populated via scalar subqueries)
    likes_count: int = 0
    comments_count: int = 0
    is_liked_by_current_user: bool = False

    model_config = ConfigDict(from_attributes=True)



class BlogPostAdminRead(BlogPostRead):
    """Full blog post response for admins — includes moderation details."""
    approved_by: UUID | None
    rejection_reason: str | None
