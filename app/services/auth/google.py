from app.models.user_profile import UserProfile
from app.repositories.users.get_user_by_provider_id import get_user_by_provider_id
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


async def find_or_create_google_user(db: AsyncSession, user_info: dict) -> User:
    """
    Resolve a Google user_info dict to a local User and Profile record.

    Strategy:
    1. Look up by provider + provider_user_id  → existing Google user
    2. Create a brand-new User + UserProfile
    """
    google_sub = user_info["sub"]
    email = user_info["email"]
    full_name = user_info.get("name")
    avatar_url = user_info.get("picture")

    # 1. Existing Google-linked account
    user_result = await get_user_by_provider_id(db, "google", google_sub)
    if user_result:
        logger.info("Google login: found existing user %s", user_result.id)
        await db.refresh(user_result, ["profile"])

        # Backfill a profile for users created before the profile split
        if user_result.profile is None:
            logger.info("Backfilling profile for existing user %s", user_result.id)
            profile = UserProfile(
                user_id=user_result.id,
                full_name=full_name,
                avatar_url=avatar_url,
            )
            db.add(profile)
            await db.commit()
            await db.refresh(user_result, ["profile"])

        return user_result

    # 2. Brand-new user
    logger.info("Google login: creating new user and profile for %s", email)
    
    # Create the base User
    user = User(
        email=email,
        provider="google",
        provider_user_id=google_sub,
    )
    db.add(user)
    await db.flush()  # Extract user.id before creating profile

    # Create the associated Profile
    profile = UserProfile(
        user_id=user.id,
        full_name=full_name,
        avatar_url=avatar_url,
    )
    db.add(profile)
    
    await db.commit()
    await db.refresh(user, ["profile"])
    return user
