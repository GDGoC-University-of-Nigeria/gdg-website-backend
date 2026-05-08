"""POST /api/v1/admin/projects/{project_id}/reject — Admin reject a project."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.project import ProjectApprovalStatus
from app.models.user import User
from app.repositories.projects import get_project_by_id, reject_project
from app.schemas.project import ProjectApproveReject, ProjectRead
from .router import router


@router.post("/{project_id}/reject", response_model=ProjectRead)
async def admin_reject_project(
    payload: ProjectApproveReject,
    project_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Reject a pending project, hiding it from public listings.

    An optional rejection reason can be provided to inform the creator.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if project.approval_status == ProjectApprovalStatus.rejected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project is already rejected",
        )

    return await reject_project(db=db, project=project, reason=payload.reason)
