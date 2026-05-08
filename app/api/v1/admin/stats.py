"""GET /api/v1/admin/stats — Dashboard aggregate stats for admins."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.user import User
from app.repositories.admin import get_stats
from app.schemas.admin import AdminStatsResponse


router = APIRouter(prefix="/admin", tags=["admin stats"])


@router.get("/stats", response_model=AdminStatsResponse)
async def admin_get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """
    Get aggregate metrics for the admin dashboard.
    - Requires admin privileges.
    """
    return await get_stats(db)
