"""PATCH /api/v1/admin/projects/{project_id}/feature — Admin feature/unfeature a project."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.project import ProjectApprovalStatus
from app.models.user import User
from app.repositories.projects import feature_project, get_project_by_id
from app.schemas.project import ProjectFeatureToggle, ProjectRead
from .router import router


@router.patch("/{project_id}/feature", response_model=ProjectRead)
async def admin_feature_project(
    payload: ProjectFeatureToggle,
    project_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Feature or un-feature a project on the public listing.

    Only **approved** projects can be featured. Featuring a rejected or
    pending project is not allowed.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if project.approval_status != ProjectApprovalStatus.approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved projects can be featured",
        )

    return await feature_project(db=db, project=project, is_featured=payload.is_featured)
