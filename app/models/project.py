"""
Project model for the GDGoC UNN API.

This module defines the Project model and ProjectStatus enum for managing
open-source projects and collaborative initiatives within the GDGoC UNN community.
"""

from sqlalchemy import Column, String, Date, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
import uuid
import enum


class ProjectStatus(str, enum.Enum):
    """
    Enumeration of possible project statuses.
    
    Attributes:
        ongoing: Project is currently active and accepting contributions
        completed: Project has been finished and is no longer active
    """
    ongoing = "ongoing"
    completed = "completed"


class Project(Base):
    """
    Project model representing an open-source or collaborative project.
    
    Projects are community initiatives where members can collaborate on building
    software, tools, or other technical solutions. Members can apply to join
    projects as contributors with specific roles.
    
    Attributes:
        id (UUID): Unique identifier for the project
        title (str): Project name
        description (str): Detailed description of the project and its goals
        duration (str, optional): Expected project duration (e.g., "3 months", "6 weeks")
        start_date (date, optional): Project start date
        end_date (date, optional): Project completion/deadline date
        github_repo (str, optional): GitHub repository URL
        demo_video_url (str, optional): URL to project demo or presentation video
        status (ProjectStatus): Current project status (ongoing/completed)
        created_at (datetime): Timestamp when the project was created
    
    Relationships:
        creator: User who created this project (to be implemented)
        applicants: Users who applied to contribute to this project
        contributors: Approved contributors working on this project (to be implemented)
    """
    
    __tablename__ = "projects"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Project information
    title = Column(String, nullable=False)  # Project name
    description = Column(String, nullable=False)  # Project description and goals
    duration = Column(String, nullable=True)  # Expected duration (e.g., "3 months")

    # Timeline
    start_date = Column(Date, nullable=True)  # Project start date
    end_date = Column(Date, nullable=True)  # Project end/deadline date

    # Resources
    github_repo = Column(String, nullable=True)  # GitHub repository link
    demo_video_url = Column(String, nullable=True)  # Demo/presentation video

    # Status and metadata
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ongoing)  # Project status
    created_at = Column(DateTime, server_default=func.now())  # Creation timestamp

    # Relationships (to be implemented)
    # creator = relationship("User", back_populates="projects")
    # applicants = relationship("Applicant", back_populates="project")
    # contributors = relationship("ProjectContributor", back_populates="project")
