from pydantic import BaseModel, EmailStr
from typing import List, Literal
from uuid import UUID



# class UserCreate(BaseModel):
#     id: UUID
#     full_name: str | None
#     email: EmailStr
#     provider: Literal["google"]
#     provider_user_id: str

   


class UserRead(BaseModel):
   
  
    id: UUID
    email: EmailStr
    full_name: str | None
    # role: str | None
    # github: str | None
    # avatar_url: str | None
    skills: List[str]

    class Config:
        from_attributes = True