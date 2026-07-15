from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.db.session import get_db
from app.models.hackathon import HackathonRegistration
from app.schemas.hackathon import HackathonRegistrationCreate, HackathonRegistrationResponse

router = APIRouter()

@router.post("/register", response_model=HackathonRegistrationResponse)
async def register_for_hackathon(
    *,
    db: AsyncSession = Depends(get_db),
    registration_in: HackathonRegistrationCreate,
) -> Any:
    """
    Register a user or team for the hackathon.
    """
    # Create the registration record
    db_registration = HackathonRegistration(
        full_name=registration_in.full_name,
        email=registration_in.email,
        github_link=registration_in.github_link,
        team_name=registration_in.team_name,
        user_id=None,
    )
    db.add(db_registration)
    await db.commit()
    await db.refresh(db_registration)
    return db_registration
