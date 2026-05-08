"""DELETE /api/v1/projects/me/applications/{id} — Withdraw an application."""

from uuid import UUID
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.applicants import delete_application, get_application_by_id
from .router import router


@router.delete("/me/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_project_application(
    application_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Withdraw a project application.
    
    - Only the **applicant** can withdraw their own application.
    - Application can only be withdrawn if not yet approved (is_contributor is False).
    """
    application = await get_application_by_id(db, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only withdraw your own applications",
        )

    if application.is_contributor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot withdraw an application that has already been approved",
        )

    await delete_application(db=db, application=application)
