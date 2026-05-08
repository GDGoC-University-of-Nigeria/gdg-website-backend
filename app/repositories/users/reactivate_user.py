"""Reactivate a previously deactivated user account."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def reactivate_user(db: AsyncSession, user: User) -> User:
    """Set is_active = True on a deactivated user."""
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    return user
