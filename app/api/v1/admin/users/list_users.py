from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.require_admin import require_admin
from app.repositories.users.get_all_users import get_all_users
from app.schemas.user import UserResponse
from app.db.session import get_db

router = APIRouter(prefix="/admin/users", tags=["admin users list"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return await get_all_users(db)
