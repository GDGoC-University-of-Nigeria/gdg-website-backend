"""Comment schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommentAuthorInfo(BaseModel):
    """Minimal author info for comment display."""
    id: UUID
    full_name: str | None
    email: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentRead(BaseModel):
    id: UUID
    content: str
    user_id: UUID
    blogpost_id: UUID
    created_at: datetime | None
    updated_at: datetime | None
    author: CommentAuthorInfo | None = Field(default=None, validation_alias="user")

    model_config = ConfigDict(from_attributes=True)
