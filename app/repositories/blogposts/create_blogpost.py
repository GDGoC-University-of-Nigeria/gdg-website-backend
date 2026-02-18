from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.blogpost import BlogPost, BlogPostStatus
from app.schemas.blogpost import BlogPostCreate


async def create_blogpost(
    db: AsyncSession,
    payload: BlogPostCreate,
    author_id: UUID,
    auto_approve: bool = False,
) -> BlogPost:
    now = datetime.utcnow()  # naive UTC — matches TIMESTAMP WITHOUT TIME ZONE

    post = BlogPost(
        author_id=author_id,
        title=payload.title,
        content=payload.content,
        image_url=payload.image_url,
        niche=payload.niche,
        status=BlogPostStatus.approved if auto_approve else BlogPostStatus.pending,
        approved_by=author_id if auto_approve else None,
        approved_at=now if auto_approve else None,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

