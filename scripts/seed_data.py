"""
Seed script for events, projects, and blog posts.
Run after create_admin.py. Creates sample data for development/demo.
"""
import asyncio
from datetime import date, time, timedelta

# Register all models before using (required for SQLAlchemy relationships)
import app.db.base_class  # noqa: F401

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.repositories.events import create_event
from app.repositories.projects import create_project
from app.repositories.blogposts import create_blogpost
from app.schemas.event import EventCreate
from app.schemas.project import ProjectCreate, ProjectType
from app.schemas.blogpost import BlogPostCreate


async def get_or_create_admin(db) -> User:
    """Get existing admin or create one."""
    result = await db.execute(select(User).where(User.email == "admin@example.com"))
    user = result.scalars().first()
    if user:
        print("Using existing admin:", user.email)
        return user
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
    await db.refresh(user)
    print("Created admin:", user.email)
    return user


async def seed_events(db, admin_id):
    """Seed 3-5 sample events."""
    today = date.today()
    events_data = [
        EventCreate(
            title="GDG UNN DevFest 2025",
            description="Annual developer festival with talks, workshops, and networking.",
            date=today,
            start_time=time(9, 0),
            end_time=time(17, 0),
            image_url=None,
            location="University of Nigeria, Nsukka",
        ),
        EventCreate(
            title="Flutter Workshop",
            description="Hands-on Flutter development workshop for beginners.",
            date=date(today.year, today.month, min(today.day + 7, 28)),
            start_time=time(14, 0),
            end_time=time(17, 0),
            image_url=None,
            location="Tech Hub, UNN",
        ),
        EventCreate(
            title="Cloud & AI Meetup",
            description="Exploring Google Cloud and AI/ML tools.",
            date=date(today.year, today.month, min(today.day + 14, 28)),
            start_time=time(10, 0),
            end_time=time(12, 30),
            image_url=None,
            location="Online",
        ),
    ]
    for ev in events_data:
        await create_event(db, ev, admin_id)
    print(f"Seeded {len(events_data)} events")


async def seed_projects(db, admin_id):
    """Seed 2-3 sample projects."""
    today = date.today()
    projects_data = [
        ProjectCreate(
            project_type=ProjectType.community,
            title="GDG UNN Website",
            description="Community website for GDG UNN chapter. Built with Next.js and FastAPI.",
            duration="3 months",
            start_date=today,
            end_date=today + timedelta(days=90),
            github_repo="https://github.com/gdg-unn/website",
            demo_video_url=None,
        ),
        ProjectCreate(
            project_type=ProjectType.community,
            title="Open Source Contributions Tracker",
            description="Track and celebrate open source contributions from community members.",
            duration="6 weeks",
            start_date=today,
            end_date=None,
            github_repo=None,
            demo_video_url=None,
        ),
    ]
    for proj in projects_data:
        await create_project(db, proj, admin_id)
    print(f"Seeded {len(projects_data)} projects")


async def seed_blog_posts(db, admin_id):
    """Seed 2-3 approved blog posts."""
    posts_data = [
        BlogPostCreate(
            title="Welcome to GDG UNN",
            content="We're excited to have you here. GDG UNN is a community of developers passionate about Google technologies.",
            image_url=None,
            niche="Community",
        ),
        BlogPostCreate(
            title="Getting Started with Flutter",
            content="Flutter is Google's UI toolkit for building natively compiled applications. Here's a quick start guide.",
            image_url=None,
            niche="Mobile",
        ),
        BlogPostCreate(
            title="Cloud Computing Basics",
            content="An introduction to cloud computing and how to get started with Google Cloud Platform.",
            image_url=None,
            niche="Cloud",
        ),
    ]
    for post in posts_data:
        await create_blogpost(db, post, admin_id, auto_approve=True)
    print(f"Seeded {len(posts_data)} blog posts")


async def main():
    async with AsyncSessionLocal() as db:
        admin = await get_or_create_admin(db)
        await seed_events(db, admin.id)
        await seed_projects(db, admin.id)
        await seed_blog_posts(db, admin.id)
    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
