"""
Idempotent seed script for events, projects, blog posts, and team members.
Requires an existing admin user (created separately).
"""

import asyncio
from datetime import date, time, timedelta

import app.db.base_class  # noqa: F401

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.team_member import TeamMember
from app.models.event import Event
from app.models.project import Project
from app.models.blogpost import BlogPost
from app.repositories.events import create_event
from app.repositories.projects import create_project
from app.repositories.blogposts import create_blogpost
from app.schemas.event import EventCreate
from app.schemas.project import ProjectCreate, ProjectType
from app.schemas.blogpost import BlogPostCreate


async def get_admin(db) -> User:
    result = await db.execute(select(User).where(User.is_admin == True))
    user = result.scalars().first()
    if not user:
        raise Exception("Admin user not found. Run admin creation script first.")
    return user


async def seed_events(db, admin_id):
    today = date.today()

    existing = await db.execute(select(Event.title))
    existing_titles = set(existing.scalars().all())

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

    count = 0
    for ev in events_data:
        if ev.title not in existing_titles:
            await create_event(db, ev, admin_id)
            count += 1

    print(f"Seeded {count} new events")


async def seed_projects(db, admin_id):
    today = date.today()

    existing = await db.execute(select(Project.title))
    existing_titles = set(existing.scalars().all())

    projects_data = [
        ProjectCreate(
            project_type=ProjectType.community,
            title="GDG UNN Website",
            description="Community website for GDG UNN chapter.",
            duration="3 months",
            start_date=today,
            end_date=today + timedelta(days=90),
            github_repo="https://github.com/gdg-unn/website",
            demo_video_url=None,
        ),
        ProjectCreate(
            project_type=ProjectType.community,
            title="Open Source Contributions Tracker",
            description="Track open source contributions.",
            duration="6 weeks",
            start_date=today,
            end_date=None,
            github_repo=None,
            demo_video_url=None,
        ),
    ]

    count = 0
    for proj in projects_data:
        if proj.title not in existing_titles:
            await create_project(db, proj, admin_id)
            count += 1

    print(f"Seeded {count} new projects")


async def seed_blog_posts(db, admin_id):
    existing = await db.execute(select(BlogPost.title))
    existing_titles = set(existing.scalars().all())

    posts_data = [
        BlogPostCreate(
            title="Welcome to GDG UNN",
            content="We're excited to have you here.",
            image_url=None,
            niche="Community",
        ),
        BlogPostCreate(
            title="Getting Started with Flutter",
            content="Flutter quick start guide.",
            image_url=None,
            niche="Mobile",
        ),
        BlogPostCreate(
            title="Cloud Computing Basics",
            content="Intro to cloud computing.",
            image_url=None,
            niche="Cloud",
        ),
    ]

    count = 0
    for post in posts_data:
        if post.title not in existing_titles:
            await create_blogpost(db, post, admin_id, auto_approve=True)
            count += 1

    print(f"Seeded {count} new blog posts")


async def seed_team_members(db):
    existing = await db.execute(select(TeamMember.name))
    existing_names = set(existing.scalars().all())

    members_data = [
        {"name": "Ndubuisi Mark", "role": "Lead", "display_order": 1},
        {"name": "Nzeribe Mmesoma", "role": "Operations Lead", "display_order": 2},
        {"name": "Perpetual Asogwa", "role": "Technical Lead", "display_order": 3},
        {"name": "Solomon Adzape", "role": "Technical Lead", "display_order": 4},
        {"name": "Chidinma Ajima", "role": "Community Manager", "display_order": 5},
        {"name": "Igwe Favour", "role": "Designer", "display_order": 6},
        {"name": "Somto Ufodiama", "role": "Designer", "display_order": 7},
        {"name": "Ihuoma Obasi", "role": "Social Media Manager", "display_order": 8},
    ]

    count = 0
    for m in members_data:
        if m["name"] not in existing_names:
            db.add(TeamMember(**m, image_url=None))
            count += 1

    await db.commit()
    print(f"Seeded {count} new team members")


async def main():
    async with AsyncSessionLocal() as db:
        admin = await get_admin(db)
        await seed_events(db, admin.id)
        await seed_projects(db, admin.id)
        await seed_blog_posts(db, admin.id)
        await seed_team_members(db)

    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
