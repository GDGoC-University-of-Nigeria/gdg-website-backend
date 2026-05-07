"""GET /me/applications — Get the current user's project applications."""

from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.applicants import get_user_applications
from app.schemas.applicant import ApplicantRead
from .router import router


@router.get("/me/applications", response_model=List[ApplicantRead])
async def my_applications_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all project applications for the current user."""
    return await get_user_applications(db=db, user_id=current_user.id)
