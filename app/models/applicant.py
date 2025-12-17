"""
Applicant model for the GDGoC UNN API.

This module defines the Applicant model for managing project collaboration
applications and contributor approvals.
"""

from sqlalchemy import Column, Boolean, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from sqlalchemy.sql import func
import uuid


class Applicant(Base):
    """
    Applicant model representing a user's application to contribute to a project.
    
    When users want to contribute to a project, they submit an application specifying
    their desired role. Project owners can review applications and approve contributors.
    Once approved, the is_contributor flag is set to True.
    
    Attributes:
        id (UUID): Unique identifier for the application
        user_id (UUID): ID of the user applying to the project
        project_id (UUID): ID of the project being applied to
        role (str): Desired role in the project (e.g., "Frontend Developer", "Designer")
        is_contributor (bool): Whether the application has been approved
        applied_at (datetime): Timestamp when the application was submitted
    
    Relationships:
        user: User who submitted this application (to be implemented)
        project: Project this application is for (to be implemented)
    
    Workflow:
        1. User submits application with desired role (is_contributor=False)
        2. Project owner reviews application
        3. If approved, is_contributor is set to True
        4. User gains contributor access to the project
    """
    
    __tablename__ = "applicants"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # Applicant
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)  # Target project

    # Application details
    role = Column(String, nullable=False)  # Desired role in the project
    is_contributor = Column(Boolean, default=False)  # Approval status
    
    # Metadata
    applied_at = Column(DateTime, server_default=func.now())  # Application timestamp

    # Relationships (to be implemented)
    # user = relationship("User", back_populates="applications")
    # project = relationship("Project", back_populates="applicants")
