"""
Project model for the GDGoC UNN API.

This module defines the Project model and ProjectStatus enum for managing
open-source projects and collaborative initiatives within the GDGoC UNN community.
"""

from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid
import enum


class ProjectStatus(str, enum.Enum):
    ongoing = "ongoing"
    completed = "completed"


class ProjectApprovalStatus(str, enum.Enum):
    """
    Admin-controlled approval state for projects.
     
    """
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ProjectType(str, enum.Enum):
    """
    Enumeration of project types.
    
    Attributes:
        personal: Project created by a regular community member
        community: Official community project created by an admin
    """
    personal = "personal"
    community = "community"


class Project(Base):
    
    __tablename__ = "projects"

    # Primary identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Project type and ownership
    project_type = Column(Enum(ProjectType), nullable=False) 
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False) 
    
    # Project information
    title = Column(String, nullable=False) 
    description = Column(String, nullable=False)  
    duration = Column(String, nullable=True)  

    # Timeline
    start_date = Column(Date, nullable=True) 
    end_date = Column(Date, nullable=True) 

    # Resources
    github_repo = Column(String, nullable=True) 
    demo_video_url = Column(String, nullable=True) 

    # Status and metadata
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ongoing)  
    created_at = Column(DateTime, server_default=func.now()) 

    # Admin moderation
    approval_status = Column(
        Enum(ProjectApprovalStatus, name="projectapprovalstatus"),
        nullable=False,
        default=ProjectApprovalStatus.pending,
        server_default="pending",
    )
    rejection_reason = Column(Text, nullable=True)
    is_featured = Column(Boolean, nullable=False, default=False, server_default="false")

    # Relationships
    creator = relationship("User", back_populates="created_projects", foreign_keys=[creator_id])
    applicants = relationship("Applicant", back_populates="project", cascade="all, delete-orphan")
    contributors = relationship("ProjectContributor", back_populates="project", cascade="all, delete-orphan")
