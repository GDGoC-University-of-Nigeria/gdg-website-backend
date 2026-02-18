"""Blogpost moderation workflow

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-02-18 17:10:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the enum type
    blogpoststatus = postgresql.ENUM(
        'pending', 'approved', 'rejected',
        name='blogpoststatus',
        create_type=False,
    )
    blogpoststatus.create(op.get_bind(), checkfirst=True)

    # 2. Create blogposts table from scratch (never existed in DB)
    op.create_table(
        'blogposts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('content_format', sa.String(), server_default='markdown', nullable=True),
        sa.Column('niche', sa.String(), nullable=True),
        sa.Column(
            'status',
            postgresql.ENUM('pending', 'approved', 'rejected', name='blogpoststatus', create_type=False),
            nullable=False,
            server_default='pending',
        ),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('rejection_reason', sa.String(), nullable=True),
        sa.Column('posted_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )

    # 3. Add index on status for efficient filtering
    op.create_index('ix_blogposts_status', 'blogposts', ['status'])


def downgrade() -> None:
    op.drop_index('ix_blogposts_status', table_name='blogposts')
    op.drop_table('blogposts')
    postgresql.ENUM('pending', 'approved', 'rejected', name='blogpoststatus').drop(
        op.get_bind(), checkfirst=True
    )
