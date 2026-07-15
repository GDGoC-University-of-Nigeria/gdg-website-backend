import asyncio
from app.db.session import engine
from app.db.base import Base
# Import all models to ensure they are registered
import app.models.user
import app.models.user_profile
import app.models.event
import app.models.event_registration
import app.models.project
import app.models.hackathon
import app.models.blogpost
import app.models.speaker
import app.models.comment
import app.models.team_member

async def main():
    async with engine.begin() as conn:
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(main())
