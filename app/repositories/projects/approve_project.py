"""Approve a project (admin workflow)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project, ProjectApprovalStatus


async def approve_project(db: AsyncSession, project: Project) -> Project:
    """Set project approval_status to approved and clear any prior rejection reason."""
    project.approval_status = ProjectApprovalStatus.approved
    project.rejection_reason = None
    await db.commit()
    await db.refresh(project)
    return project
