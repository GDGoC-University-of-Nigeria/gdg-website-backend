from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blogpost import BlogPost, BlogPostStatus


async def reject_blogpost(
    db: AsyncSession,
    post: BlogPost,
    rejection_reason: str | None = None,
) -> BlogPost:
    post.status = BlogPostStatus.rejected
    post.rejection_reason = rejection_reason
    post.approved_by = None
    post.approved_at = None
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
