from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def update_user(
    db: AsyncSession,
    user_id: UUID,
    *,
    full_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
) -> User | None:
    """Update user by ID. Only updates provided non-None fields."""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        return None

    if full_name is not None:
        user.full_name = full_name
    if email is not None:
        # Check email not taken by another user
        existing = (await db.execute(select(User).where(User.email == email, User.id != user_id))).scalars().first()
        if existing:
            await db.rollback()
            raise ValueError("Email already in use")
        user.email = email
    if phone is not None:
        user.phone = phone.strip() or None

    await db.commit()
    await db.refresh(user)
    return user
