"""Reject a project (admin workflow)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectApprovalStatus


async def reject_project(
    db: AsyncSession,
    project: Project,
    reason: str | None = None,
) -> Project:
    """Set project approval_status to rejected and store the optional reason."""
    project.approval_status = ProjectApprovalStatus.rejected
    project.rejection_reason = reason
    await db.commit()
    await db.refresh(project)
    return project
