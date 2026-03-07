"""GET /api/v1/admin/blogposts — Admin: list posts filtered by status."""

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.blogpost import BlogPostStatus
from app.repositories.blogposts import get_posts_by_status_with_author
from app.schemas.blogpost import BlogPostAdminRead
from .router import router


@router.get("/", response_model=list[BlogPostAdminRead])
async def admin_list_blogposts(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_admin),
    status_param: str | None = Query(None, alias="status", description="Filter by status: pending, approved, rejected, or all"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    Admin: list all blog posts, optionally filtered by status.

    Use `?status=pending` to see the moderation queue. Omit status or use status=all for all posts.
    Returns posts with author (user) loaded for display.
    """
    status = None
    if status_param and status_param != "all":
        try:
            status = BlogPostStatus(status_param)
        except ValueError:
            status = None  # Invalid value treated as no filter
    return await get_posts_by_status_with_author(db=db, status=status, skip=skip, limit=limit)
