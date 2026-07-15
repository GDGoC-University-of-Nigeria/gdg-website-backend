# scripts/create_admin.py
import asyncio

# Register all models before using User (required for SQLAlchemy relationships)
import app.db.base_class  # noqa: F401

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password

async def create_admin():
    async with AsyncSessionLocal() as db:
        user = User(
            email="admin@example.com",
            full_name="Admin",
            hashed_password=hash_password("YourSecurePassword123!"),
            is_admin=True,
            provider="local",
            provider_user_id="admin@example.com",
        )
        db.add(user)
        await db.commit()
        print("Admin created:", user.email)

if __name__ == "__main__":
    asyncio.run(create_admin())