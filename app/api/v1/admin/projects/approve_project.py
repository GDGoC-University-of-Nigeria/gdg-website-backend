"""POST /api/v1/admin/projects/{project_id}/approve — Admin approve a project."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.project import ProjectApprovalStatus
from app.models.user import User
from app.repositories.projects import approve_project, get_project_by_id
from app.schemas.project import ProjectRead
from .router import router


@router.post("/{project_id}/approve", response_model=ProjectRead)
async def admin_approve_project(
    project_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Approve a pending project, making it publicly visible.

    - Only `pending` or `rejected` projects can be approved.
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if project.approval_status == ProjectApprovalStatus.approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project is already approved",
        )

    return await approve_project(db=db, project=project)
