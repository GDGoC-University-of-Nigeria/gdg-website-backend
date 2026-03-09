"""POST /{project_id}/apply — Apply to contribute to a project."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.projects.get_project_by_id import get_project_by_id
from app.repositories.applicants import create_application
from app.schemas.applicant import ApplicantRead
from .router import router


class ApplyPayload(BaseModel):
    role: str


@router.post(
    "/{project_id}/apply",
    response_model=ApplicantRead,
    status_code=status.HTTP_201_CREATED,
)
async def apply_endpoint(
    payload: ApplyPayload,
    project_id: UUID = Path(..., description="Project ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Apply to contribute to a project."""
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if project.creator_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You own this project")
    try:
        return await create_application(
            db=db, user_id=current_user.id, project_id=project_id, role=payload.role,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
