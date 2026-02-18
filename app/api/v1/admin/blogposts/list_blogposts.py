"""GET /api/v1/admin/blogposts — Admin: list posts filtered by status."""

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.require_admin import require_admin
from app.models.blogpost import BlogPostStatus
from app.repositories.blogposts import get_posts_by_status
from app.schemas.blogpost import BlogPostAdminRead
from .router import router


@router.get("/", response_model=list[BlogPostAdminRead])
async def admin_list_blogposts(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_admin),
    status: BlogPostStatus | None = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """
    Admin: list all blog posts, optionally filtered by status.

    Use `?status=pending` to see the moderation queue.
    """
    return await get_posts_by_status(db=db, status=status, skip=skip, limit=limit)
