from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Literal
from uuid import UUID
from pydantic.config import ConfigDict

class UserProfileSchema(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class UserBasic(BaseModel):
    """Shared basic user info for nested responses."""
    id: UUID
    email: EmailStr
    is_admin: bool = False
    profile: UserProfileSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):

    id: UUID
    email: EmailStr
    is_admin: bool
    created_at: datetime
    is_active: bool
    profile: UserProfileSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserRequest(BaseModel):
    """Partial update for user profile (PATCH /users/me)."""
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


class UserRoleUpdate(BaseModel):
    """Admin payload to promote or demote a user."""
    is_admin: bool


class MemberListResponse(BaseModel):
    """Paginated community member list with server-side total count."""
    total: int
    items: List[UserResponse]


class EventRegistrationRead(BaseModel):
    """Minimal registration record returned to admins."""
    id: UUID
    event_id: UUID
    user_id: UUID
    registered_at: datetime
    user: UserBasic | None = None

    model_config = ConfigDict(from_attributes=True)




