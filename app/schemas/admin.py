"""Admin dashboard aggregate schemas."""

from pydantic import BaseModel


class AdminStatsResponse(BaseModel):
    """Real-time dashboard aggregates for the admin stats endpoint."""
    total_users: int
    total_active_users: int
    total_blogposts: int
    pending_blogposts: int
    approved_blogposts: int
    total_events: int
    published_events: int
    total_projects: int
    pending_projects: int
    approved_projects: int
    total_comments: int
    pending_applications: int  # applications where is_contributor=False
