"""
Updated get_blogpost_by_id — returns post with engagement counts via scalar subqueries.
Avoids N+1 by computing counts at the SQL level in a single query.
"""

from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog_post_like import BlogPostLike
from app.models.blogpost import BlogPost
from app.models.comment import Comment


async def get_blogpost_by_id(
    db: AsyncSession,
    post_id: UUID,
    current_user_id: UUID | None = None,
) -> dict | None:
    likes_sq = (
        select(func.count())
        .where(BlogPostLike.blogpost_id == BlogPost.id)
        .scalar_subquery()
    )
    comments_sq = (
        select(func.count())
        .where(Comment.blogpost_id == BlogPost.id)
        .scalar_subquery()
    )
    is_liked_sq = (
        select(func.count())
        .where(
            BlogPostLike.blogpost_id == BlogPost.id,
            BlogPostLike.user_id == current_user_id,
        )
        .scalar_subquery()
        if current_user_id
        else None
    )

    if is_liked_sq is not None:
        stmt = select(
            BlogPost,
            likes_sq.label("likes_count"),
            comments_sq.label("comments_count"),
            is_liked_sq.label("is_liked"),
        ).where(BlogPost.id == post_id)
    else:
        stmt = select(
            BlogPost,
            likes_sq.label("likes_count"),
            comments_sq.label("comments_count"),
        ).where(BlogPost.id == post_id)

    result = await db.execute(stmt)
    row = result.first()
    if not row:
        return None

    post = row[0]
    likes_count = row[1]
    comments_count = row[2]
    is_liked = bool(row[3]) if is_liked_sq is not None else False

    return {
        **{c.key: getattr(post, c.key) for c in post.__table__.columns},
        "likes_count": likes_count,
        "comments_count": comments_count,
        "is_liked_by_current_user": is_liked,
    }
