"""DELETE /{project_id}/applications/{applicant_id} — Reject/remove an application."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from app.repositories.applicants import reject_application
from .router import router


@router.delete(
    "/{project_id}/applications/{applicant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def reject_application_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    applicant_id: UUID = Path(..., description="Applicant ID"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """Reject an application. Project owner or admin only."""
    deleted = await reject_application(db=db, applicant_id=applicant_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
