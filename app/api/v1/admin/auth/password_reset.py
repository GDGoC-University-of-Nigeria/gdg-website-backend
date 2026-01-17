from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.require_admin import require_admin
from app.schemas.admin.auth.password_reset import AdminResetPasswordRequest
from app.db.session import get_db
from app.services.admin.auth.password_reset import reset_user_password

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Auth"])

@router.post("/reset-password")
async def admin_reset_password(
    data: AdminResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
):
    await reset_user_password(
        db=db,
        email=admin.email,
        new_password=data.new_password,
    )
    print(f"Received body: {data}")
    return {"detail": "Password reset successful"}
