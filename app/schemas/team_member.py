from pydantic import BaseModel
from pydantic.config import ConfigDict


class TeamMemberResponse(BaseModel):
    id: str
    name: str
    role: str
    image_url: str | None

    model_config = ConfigDict(from_attributes=True)
