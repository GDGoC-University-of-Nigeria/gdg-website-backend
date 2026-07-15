import asyncio
from sqlalchemy import text
from app.db.session import engine

async def main():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    await engine.dispose()
    print("Dropped alembic_version")

if __name__ == "__main__":
    asyncio.run(main())
