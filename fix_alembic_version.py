"""
Script to fix Alembic version mismatch on Render database.

This script will:
1. Connect to the Render database
2. Delete the invalid alembic_version entry
3. Insert the correct version (9138ab93e79b - the latest migration)
"""
import asyncio
import asyncpg

async def fix_alembic_version():
    # Render database URL
    DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_9nbMKV5ZPhFu@ep-sweet-truth-aic0ba6i-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    # Connect to database (remove +asyncpg from URL for asyncpg)
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Check current version
        current_version = await conn.fetchval("SELECT version_num FROM alembic_version")
        print(f"Current version in database: {current_version}")
        
        # Delete the invalid version
        await conn.execute("DELETE FROM alembic_version")
        print("Deleted invalid version")
        
        # Insert the correct latest version
        latest_version = "9138ab93e79b"  # Your latest migration
        await conn.execute(
            "INSERT INTO alembic_version (version_num) VALUES ($1)",
            latest_version
        )
        print(f"Set version to: {latest_version}")
        
        # Verify
        new_version = await conn.fetchval("SELECT version_num FROM alembic_version")
        print(f"New version in database: {new_version}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_alembic_version())
