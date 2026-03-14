"""GET /api/v1/team - List team members (builders) for landing page. Public, no auth."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.team_member import TeamMember
from app.schemas.team_member import TeamMemberResponse
from fastapi import Depends

from .router import router


@router.get("", response_model=list[TeamMemberResponse])
async def list_team(
    db: AsyncSession = Depends(get_db),
):
    """List team members ordered by display_order. Used by landing page builders section."""
    result = await db.execute(
        select(TeamMember).order_by(TeamMember.display_order.asc(), TeamMember.name.asc())
    )
    return result.scalars().all()
