"""
ProjectContributor model for the GDGoC UNN API.

This module defines the ProjectContributor model for managing approved contributors
to projects. This is separate from the Applicant model - applicants who get approved
are added to this table as contributors.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid


class ProjectContributor(Base):
    """
    ProjectContributor model representing an approved contributor to a project.
    
    Contributors are users who have been added to a project by the project creator.
    They have specific roles within the project (e.g., Frontend Developer, Designer).
    This is separate from applicants - once an applicant is approved or a user is
    directly added, they become a contributor.
    
    Attributes:
        id (UUID): Unique identifier for the contributor record
        project_id (UUID): ID of the project
        user_id (UUID): ID of the contributor user
        role (str): Contributor's role in the project (e.g., "Frontend Developer")
        added_at (datetime): Timestamp when the user was added as a contributor
    
    Relationships:
        project: Project this contributor belongs to
        user: User who is the contributor
    
    Constraints:
        - Unique constraint on (project_id, user_id) to prevent duplicate contributors
    """
    
    __tablename__ = "project_contributors"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign keys
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Contributor details
    role = Column(String, nullable=False)  # Contributor's role in the project
    
    # Metadata
    added_at = Column(DateTime, server_default=func.now())  # When added as contributor

    # Relationships
    project = relationship("Project", back_populates="contributors")
    user = relationship("User", back_populates="contributed_projects")

    # Constraints
    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="unique_project_contributor"),
    )
