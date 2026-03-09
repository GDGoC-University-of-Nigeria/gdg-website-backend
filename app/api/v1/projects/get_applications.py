"""GET /{project_id}/applications — List applications for a project (owner/admin)."""

from typing import List
from uuid import UUID

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_project_owner import require_project_owner
from app.models.user import User
from app.models.project import Project
from app.repositories.applicants import get_project_applications
from app.schemas.applicant import ApplicantRead
from .router import router


@router.get("/{project_id}/applications", response_model=List[ApplicantRead])
async def list_applications_endpoint(
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    auth_data: tuple[User, Project] = Depends(require_project_owner),
):
    """List all applications for a project. Project owner or admin only."""
    return await get_project_applications(db=db, project_id=project_id)
