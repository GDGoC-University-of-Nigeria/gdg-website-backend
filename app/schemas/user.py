from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Literal
from uuid import UUID
from pydantic.config import ConfigDict

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    phone: str | None
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserRequest(BaseModel):
    """Partial update for user profile (PATCH /users/me)."""
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class UpdateUserRequest(BaseModel):
    """Partial update for user profile (PATCH /users/me)."""
    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None



# class UserRead(BaseModel):
   
  
#     id: UUID
#     email: EmailStr
#     full_name: str | None
#     # role: str | None
#     # github: str | None
#     # avatar_url: str | None
#     skills: List[str]

#     class Config:
#         from_attributes = True