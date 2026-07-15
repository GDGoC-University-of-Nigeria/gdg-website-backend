from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class HackathonRegistrationCreate(BaseModel):
    full_name: str
    email: EmailStr
    github_link: Optional[str] = None
    team_name: Optional[str] = None

class HackathonRegistrationResponse(HackathonRegistrationCreate):
    id: str
    user_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
