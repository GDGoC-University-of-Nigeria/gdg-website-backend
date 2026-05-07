import uuid
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    image_url = Column(String(512), nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
