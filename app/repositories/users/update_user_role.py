"""Update a user's admin role (promote / demote)."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User


async def update_user_role(
    db: AsyncSession,
    user: User,
    is_admin: bool,
) -> User:
    """Set the is_admin flag on the given user."""
    user.is_admin = is_admin
    await db.commit()
    await db.refresh(user)
    return user
