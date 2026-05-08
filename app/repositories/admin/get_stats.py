"""Admin stats repository — single-query aggregates for the dashboard."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applicant import Applicant
from app.models.blogpost import BlogPost, BlogPostStatus
from app.models.comment import Comment
from app.models.event import Event
from app.models.project import Project, ProjectApprovalStatus
from app.models.user import User
from app.schemas.admin import AdminStatsResponse


async def get_stats(db: AsyncSession) -> AdminStatsResponse:
    """Run all aggregate queries and return the dashboard stats object."""

    async def count(stmt) -> int:
        result = await db.execute(stmt)
        return result.scalar_one()

    total_users = await count(select(func.count()).select_from(User))
    total_active_users = await count(
        select(func.count()).select_from(User).where(User.is_active.is_(True))
    )
    total_blogposts = await count(select(func.count()).select_from(BlogPost))
    pending_blogposts = await count(
        select(func.count()).select_from(BlogPost).where(BlogPost.status == BlogPostStatus.pending)
    )
    approved_blogposts = await count(
        select(func.count()).select_from(BlogPost).where(BlogPost.status == BlogPostStatus.approved)
    )
    total_events = await count(select(func.count()).select_from(Event))
    published_events = await count(
        select(func.count()).select_from(Event).where(Event.is_published.is_(True))
    )
    total_projects = await count(select(func.count()).select_from(Project))
    pending_projects = await count(
        select(func.count()).select_from(Project).where(
            Project.approval_status == ProjectApprovalStatus.pending
        )
    )
    approved_projects = await count(
        select(func.count()).select_from(Project).where(
            Project.approval_status == ProjectApprovalStatus.approved
        )
    )
    total_comments = await count(select(func.count()).select_from(Comment))
    pending_applications = await count(
        select(func.count()).select_from(Applicant).where(Applicant.is_contributor.is_(False))
    )

    return AdminStatsResponse(
        total_users=total_users,
        total_active_users=total_active_users,
        total_blogposts=total_blogposts,
        pending_blogposts=pending_blogposts,
        approved_blogposts=approved_blogposts,
        total_events=total_events,
        published_events=published_events,
        total_projects=total_projects,
        pending_projects=pending_projects,
        approved_projects=approved_projects,
        total_comments=total_comments,
        pending_applications=pending_applications,
    )
