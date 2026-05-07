from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
import app.db.base_class  # noqa: F401 — registers all models with SQLAlchemy mapper
from app.api.v1.auth.refresh import router as refresh_router
from app.api.v1.auth.google import router as google_auth_router
from app.api.v1.auth.logout import router as logout_router
from app.api.v1.events.router import router as events_router
from app.api.v1.admin.users.list_users import router as list_users_router
from app.api.v1.users.me import router as me_router
from app.api.v1.projects.router import router as projects_router
from app.api.v1.blogposts.router import router as blogposts_router
from app.api.v1.admin.blogposts.router import router as admin_blogposts_router
from app.api.v1.comments.router import router as comments_router
from app.api.v1.community import router as community_router
from app.api.v1.team import router as team_router
from app.api.v1.public_forms import router as public_forms_router
from app.api.v1.media.upload import router as media_router

app = FastAPI(title="Google Developer Group on Campus, UNN Community API")

# ── Middleware (Starlette applies them in reverse order, so the LAST
#    middleware added is the OUTERMOST wrapper – we want Session outermost) ──

# 1) CORS — added first so it is the inner layer
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Session — added AFTER CORS so it is the OUTERMOST wrapper.
#    This ensures the session cookie (used by Authlib to store OAuth state)
#    is read/written on every request, including the Google callback redirect.
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=settings.COOKIE_SECURE,   # False locally for http://localhost
)

# # Include API routes
app.include_router(refresh_router, tags=["auth"])
app.include_router(logout_router, tags=["auth"])
app.include_router(google_auth_router, tags=["auth"])
app.include_router(events_router, tags=["events"])
app.include_router(list_users_router, tags=["admin users list"])
app.include_router(me_router, tags=["me"])
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(blogposts_router, prefix="/api/v1/blogposts", tags=["blogposts"])
app.include_router(admin_blogposts_router, prefix="/api/v1/admin/blogposts", tags=["admin blogposts"])
app.include_router(comments_router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(community_router, prefix="/api/v1/community", tags=["community"])
app.include_router(team_router, prefix="/api/v1", tags=["team"])
app.include_router(public_forms_router)
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])

@app.get("/")
async def root():
    return {"message": "Welcome to the GDGoC, UNN Community API!"}