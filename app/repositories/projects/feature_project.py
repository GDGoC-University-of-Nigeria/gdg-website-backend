"""Toggle the is_featured flag on a project (admin only)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


async def feature_project(
    db: AsyncSession,
    project: Project,
    is_featured: bool,
) -> Project:
    """Set the project's is_featured flag to the given value."""
    project.is_featured = is_featured
    await db.commit()
    await db.refresh(project)
    return project
