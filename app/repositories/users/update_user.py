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
    avatar_url: str | None = None,
    bio: str | None = None,
) -> User | None:
    """Update user by ID. Updates User (email) and UserProfile (rest)."""
    # Load user with profile
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        return None
    
    # Ensure profile exists (it should, but just in case)
    await db.refresh(user, ["profile"])
    if not user.profile:
        from app.models.user_profile import UserProfile
        user.profile = UserProfile(user_id=user.id)
        db.add(user.profile)

    # Update User fields
    if email is not None:
        # Check email not taken by another user
        existing_stmt = select(User).where(User.email == email, User.id != user_id)
        existing = (await db.execute(existing_stmt)).scalars().first()
        if existing:
            await db.rollback()
            raise ValueError("Email already in use")
        user.email = email

    # Update Profile fields
    if full_name is not None:
        user.profile.full_name = full_name
    if phone is not None:
        user.profile.phone = phone.strip() or None
    if avatar_url is not None:
        user.profile.avatar_url = avatar_url
    if bio is not None:
        user.profile.bio = bio

    await db.commit()
    await db.refresh(user, ["profile"])
    return user

