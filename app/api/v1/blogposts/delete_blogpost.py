"""DELETE /api/v1/blogposts/{post_id} — Author delete their own post."""

from uuid import UUID

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.repositories.blogposts import delete_blogpost, get_blogpost_by_id
from .router import router


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def author_delete_blogpost(
    post_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Permanently delete a blog post.

    - The **author** can delete their own post (any status).
    - An **admin** can also delete any post via this route.
    """
    post = await get_blogpost_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")

    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post",
        )

    await delete_blogpost(db=db, post=post)
