from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.hackathon import HackathonRegistration
from app.schemas.hackathon import HackathonRegistrationResponse

router = APIRouter()

@router.get("/", response_model=List[HackathonRegistrationResponse])
async def get_hackathon_registrations(
    *,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all hackathon registrations.
    """
    result = await db.execute(select(HackathonRegistration).offset(skip).limit(limit))
    registrations = result.scalars().all()
    return registrations
