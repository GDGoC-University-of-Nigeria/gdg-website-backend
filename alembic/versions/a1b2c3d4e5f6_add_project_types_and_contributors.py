"""Add project types and contributors

Revision ID: ${revision_id}
Revises: 9138ab93e79b
Create Date: 2026-02-11 17:18:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '2f6808d70b5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enums
    project_status_enum = postgresql.ENUM('ongoing', 'completed', name='projectstatus', create_type=False)
    project_status_enum.create(op.get_bind(), checkfirst=True)

    project_type_enum = postgresql.ENUM('personal', 'community', name='projecttype', create_type=False)
    project_type_enum.create(op.get_bind(), checkfirst=True)

    # Create projects table (never existed before)
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_type', postgresql.ENUM('personal', 'community', name='projecttype', create_type=False), nullable=False),
        sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('duration', sa.String(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('github_repo', sa.String(), nullable=True),
        sa.Column('demo_video_url', sa.String(), nullable=True),
        sa.Column('status', postgresql.ENUM('ongoing', 'completed', name='projectstatus', create_type=False), server_default='ongoing', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['creator_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create project_contributors table
    op.create_table(
        'project_contributors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('added_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'user_id', name='unique_project_contributor'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('project_contributors')
    op.drop_table('projects')

    postgresql.ENUM('personal', 'community', name='projecttype').drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM('ongoing', 'completed', name='projectstatus').drop(op.get_bind(), checkfirst=True)

