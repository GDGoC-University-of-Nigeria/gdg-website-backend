from app.models.user_profile import UserProfile
from app.repositories.users.get_user_by_provider_id import get_user_by_provider_id
from app.repositories.users.get_user_by_email import get_user_by_email
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

    # 1. Look up by Google Provider ID (Existing Google user)
    user = await get_user_by_provider_id(db, "google", google_sub)
    
    # 2. If not found by Google ID, look up by Email (Existing user linking Google for the first time)
    # if not user:
    #     user = await get_user_by_email(db, email)
    #     if user:
    #         logger.info("Google login: linking existing user %s by email %s", user.id, email)
    #         user.provider = "google"
    #         user.provider_user_id = google_sub
    #         db.add(user) # ensure session tracking for commit
    #         # Continue to profile check/backfill
    
    if user:
        logger.info("Google login: found/linked user %s", user.id)
        
        # Ensure profile exists (backfill if missing)
        # Note: repositories usually use selectinload(User.profile), so we check if initialized
        if not user.profile:
            logger.info("Backfilling profile for user %s", user.id)
            profile = UserProfile(
                user_id=user.id,
                full_name=full_name,
                avatar_url=avatar_url,
            )
            db.add(profile)
        else:
            # Optionally update avatar if it's missing locally but provided by Google
            if not user.profile.avatar_url and avatar_url:
                user.profile.avatar_url = avatar_url
        
        await db.commit()
        await db.refresh(user, ["profile"])
        return user

    # 3. Brand-new user
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
