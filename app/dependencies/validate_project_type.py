"""
Dependency for validating project type against user role.

This ensures that:
- Regular users can only create Personal projects
- Admin users can only create Community projects
"""

from fastapi import Depends, HTTPException, status

from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectType


async def validate_project_type_for_user(
    payload: ProjectCreate,
    current_user: User = Depends(get_current_user),
) -> ProjectCreate:
    """
    Validate that the user can create the requested project type.
    
    Args:
        payload: Project creation payload
        current_user: Currently authenticated user
    
    Returns:
        Validated payload
    
    Raises:
        HTTPException: 403 if user tries to create unauthorized project type
    """
    # Admin users can only create Community projects
    if current_user.is_admin and payload.project_type != ProjectType.community:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users can only create Community projects",
        )
    
    # Regular users can only create Personal projects
    if not current_user.is_admin and payload.project_type != ProjectType.personal:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Regular users can only create Personal projects",
        )
    
    return payload
