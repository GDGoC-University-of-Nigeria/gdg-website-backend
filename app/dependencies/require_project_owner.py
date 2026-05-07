"""
Dependency for requiring project ownership or admin privileges.

This ensures that only the project creator or admins can modify a project.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.dependencies.get_current_user import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.project import Project
from app.repositories.projects import get_project_by_id


async def require_project_owner(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> tuple[User, Project]:
    """
    Verify that the current user is the project owner or an admin.
    
    Authorization rules:
    - Personal projects: only the creator can modify
    - Community projects: only admins can modify
    
    Args:
        project_id: UUID of the project
        current_user: Currently authenticated user
        db: Database session
    
    Returns:
        Tuple of (user, project)
    
    Raises:
        HTTPException: 404 if project not found, 403 if unauthorized
    """
    project = await get_project_by_id(db, project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Check authorization based on project type
    is_creator = project.creator_id == current_user.id
    is_admin = current_user.is_admin
    
    # For personal projects: only the creator can modify
    # For community projects: only admins can modify
    if project.project_type.value == "personal":
        if not is_creator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the project creator can modify this project",
            )
    else:  # community project
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can modify community projects",
            )
    
    return current_user, project
