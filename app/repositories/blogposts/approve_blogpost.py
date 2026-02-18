from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.blogpost import BlogPost, BlogPostStatus


async def approve_blogpost(
    db: AsyncSession,
    post: BlogPost,
    admin_id: UUID,
) -> BlogPost:
    post.status = BlogPostStatus.approved
    post.approved_by = admin_id
    post.approved_at = datetime.utcnow()
    post.rejection_reason = None
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
