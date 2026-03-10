from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api import auth, users, events, projects
from app.core.config import settings
import app.db.base_class  # noqa: F401 — registers all models with SQLAlchemy mapper
from app.api.v1.auth.signup import router as auth_router
from app.api.v1.auth.login import router as login_router
from app.api.v1.auth.refresh import router as refresh_router
from app.api.v1.auth.logout import router as logout_router
from app.api.v1.admin.auth.login import router as admin_login_router
from app.api.v1.admin.auth.password_reset import router as admin_password_reset_router
from app.api.v1.events.router import router as events_router
from app.api.v1.admin.users.list_users import router as list_users_router
from app.api.v1.users.me import router as me_router
from app.api.v1.projects.router import router as projects_router
from app.api.v1.blogposts.router import router as blogposts_router
from app.api.v1.admin.blogposts.router import router as admin_blogposts_router
from app.api.v1.comments.router import router as comments_router
from app.api.v1.community import router as community_router

app = FastAPI(title="Google Developer Group on Campus, UNN Community API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*", 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Include API routes
app.include_router(auth_router, tags=["auth"])
app.include_router(login_router, tags=["auth"])
app.include_router(refresh_router, tags=["auth"])
app.include_router(logout_router, tags=["auth"])
app.include_router(admin_login_router, tags=["admin auth"])
app.include_router(admin_password_reset_router, tags=["admin auth"])
app.include_router(events_router, tags=["events"])
app.include_router(list_users_router, tags=["admin users list"])
app.include_router(me_router, tags=["me"])
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(blogposts_router, prefix="/api/v1/blogposts", tags=["blogposts"])
app.include_router(admin_blogposts_router, prefix="/api/v1/admin/blogposts", tags=["admin blogposts"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(community_router, prefix="/api/v1/community", tags=["community"])

@app.get("/")
async def root():
    return {"message": "Welcome to the GDGoC, UNN Community API!"}