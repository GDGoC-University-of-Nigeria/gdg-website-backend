"""GET /api/v1/blogposts/{id}/comments — Public paginated comment listing."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.blogposts import get_blogpost_by_id
from app.repositories.comments import get_comments
from app.schemas.comment import CommentRead, CommentAuthorInfo
from .router import router


@router.get("/{post_id}/comments", response_model=list[CommentRead])
async def list_comments(
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Get comments for a blog post.

    - Public endpoint — no authentication required.
    - Ordered by `created_at DESC`.
    - Paginated via `skip` / `limit`.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    comments = await get_comments(db=db, blogpost_id=post_id, skip=skip, limit=limit)
    return [
        CommentRead(
            id=c.id,
            content=c.content,
            user_id=c.user_id,
            blogpost_id=c.blogpost_id,
            created_at=c.created_at,
            updated_at=c.updated_at,
            author=CommentAuthorInfo.model_validate(c.user) if c.user else None,
        )
        for c in comments
    ]
