"""Comment schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


from app.schemas.user import UserBasic as CommentAuthorInfo



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
