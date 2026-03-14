from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def soft_delete_user(db: AsyncSession, user_id: UUID) -> None:
    stmt = (
        update(User)
        .where(User.id == user_id, User.is_active.is_(True))
        .values(is_active=False)
    )
    await db.execute(stmt)
    await db.commit()

