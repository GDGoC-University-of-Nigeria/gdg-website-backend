"""
Updated get_all_approved — includes engagement counts via scalar subqueries.
All counts are computed in a single query — no N+1.
"""

from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog_post_like import BlogPostLike
from app.models.blogpost import BlogPost, BlogPostStatus
from app.models.comment import Comment


async def get_all_approved(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    current_user_id: UUID | None = None,
) -> list[dict]:
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

    if current_user_id:
        is_liked_sq = (
            select(func.count())
            .where(
                BlogPostLike.blogpost_id == BlogPost.id,
                BlogPostLike.user_id == current_user_id,
            )
            .scalar_subquery()
        )
        stmt = select(
            BlogPost,
            likes_sq.label("likes_count"),
            comments_sq.label("comments_count"),
            is_liked_sq.label("is_liked"),
        )
    else:
        stmt = select(
            BlogPost,
            likes_sq.label("likes_count"),
            comments_sq.label("comments_count"),
        )

    stmt = (
        stmt.where(BlogPost.status == BlogPostStatus.approved)
        .order_by(BlogPost.approved_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.all()

    posts = []
    for row in rows:
        post = row[0]
        likes_count = row[1]
        comments_count = row[2]
        is_liked = bool(row[3]) if current_user_id else False
        posts.append({
            **{c.key: getattr(post, c.key) for c in post.__table__.columns},
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked_by_current_user": is_liked,
        })
    return posts
