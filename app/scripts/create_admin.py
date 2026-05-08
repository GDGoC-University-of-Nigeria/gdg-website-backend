import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import AsyncSessionLocal
import app.db.base_class
from app.models.user import User
from app.models.user_profile import UserProfile
import os


ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "ntmark2004@gmail.com")
ADMIN_FULL_NAME = os.getenv("ADMIN_NAME", "Mark Ndubuisi")

async def create_admin():
    async with AsyncSessionLocal() as session:  
        try:
            # Check if an admin already exists
            result = await session.execute(select(User).where(User.email == ADMIN_EMAIL))
            user = result.scalars().first()

            if user:
                print(f"User with email {ADMIN_EMAIL} already exists.")
                if not user.is_admin:
                    user.is_admin = True
                    await session.commit()
                    print(f"[OK] User {ADMIN_EMAIL} is now an ADMIN.")
                else:
                    print("This user is already an admin.")
                return

            # Create new admin user
            new_admin = User(
                email=ADMIN_EMAIL,
                is_admin=True,
                provider="google",
                provider_user_id=None # Will be linked on first Google login
            )
            session.add(new_admin)
            await session.flush()

            # Create associated profile
            profile = UserProfile(
                user_id=new_admin.id,
                full_name=ADMIN_FULL_NAME
            )
            session.add(profile)
            
            await session.commit()
            print(f"[OK] Admin user created successfully!")
            print(f"   Email: {ADMIN_EMAIL}")
            print(f"   NOTE: Admin must log in via Google using this email.")
            
        except Exception as e:
            print(f"[ERROR] Error creating admin: {e}")

            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(create_admin())
