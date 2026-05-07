

from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectDetailRead
from app.repositories.projects import create_project as create_project_repo
from app.dependencies.get_current_user import get_current_user
from app.dependencies.validate_project_type import validate_project_type_for_user
from app.models.user import User
from .router import router


@router.post(
    "/",
    response_model=ProjectDetailRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_endpoint(
    payload: ProjectCreate = Depends(validate_project_type_for_user),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new project.
    
    - **Personal projects**: Can be created by regular users
    - **Community projects**: Can only be created by admins
    
    The project_type in the payload determines the type of project.
    Authorization is automatically enforced based on the user's role.
    """
    return await create_project_repo(
        db=db,
        payload=payload,
        creator_id=current_user.id,
    )
