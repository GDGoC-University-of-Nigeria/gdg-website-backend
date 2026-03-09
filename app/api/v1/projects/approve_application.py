"""PATCH /{project_id}/applications/{applicant_id}/approve — Approve an application."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from app.repositories.applicants import approve_application
from app.schemas.applicant import ApplicantRead
from .router import router


@router.patch(
    "/{project_id}/applications/{applicant_id}/approve",
    response_model=ApplicantRead,
)
async def approve_application_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    applicant_id: UUID = Path(..., description="Applicant ID"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """Approve a project application and add the user as a contributor."""
    applicant = await approve_application(db=db, applicant_id=applicant_id)
    if not applicant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return applicant
