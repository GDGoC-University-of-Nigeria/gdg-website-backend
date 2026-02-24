"""Toggle like on a blog post — insert if not exists, delete if exists."""

from uuid import UUID
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog_post_like import BlogPostLike


async def toggle_like(
    db: AsyncSession,
    blogpost_id: UUID,
    user_id: UUID,
) -> dict:
    """
    Toggle a like. Returns dict with:
    - liked: bool (True if now liked, False if unliked)
    - likes_count: int
    """
    # Check if like exists
    existing = await db.execute(
        select(BlogPostLike).where(
            BlogPostLike.blogpost_id == blogpost_id,
            BlogPostLike.user_id == user_id,
        )
    )
    like = existing.scalar_one_or_none()

    if like:
        await db.execute(
            delete(BlogPostLike).where(
                BlogPostLike.blogpost_id == blogpost_id,
                BlogPostLike.user_id == user_id,
            )
        )
        liked = False
    else:
        db.add(BlogPostLike(blogpost_id=blogpost_id, user_id=user_id))
        liked = True

    await db.commit()

    # Count after mutation
    count_result = await db.execute(
        select(func.count()).where(BlogPostLike.blogpost_id == blogpost_id)
    )
    likes_count = count_result.scalar_one()

    return {"liked": liked, "likes_count": likes_count}
