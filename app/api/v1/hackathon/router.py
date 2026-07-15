from fastapi import APIRouter
from app.api.v1.hackathon import register, admin

router = APIRouter()

router.include_router(register.router, tags=["hackathon"])
router.include_router(admin.router, prefix="/admin", tags=["hackathon-admin"])
