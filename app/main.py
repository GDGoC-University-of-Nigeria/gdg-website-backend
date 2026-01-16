from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api import auth, users, events, projects
from app.core.config import settings
from app.api.v1.auth.signup import router as auth_router
from app.api.v1.auth.login import router as login_router
from app.api.v1.auth.refresh import router as refresh_router
from app.api.v1.auth.logout import router as logout_router
from app.api.v1.admin.auth.login import router as admin_login_router
from app.api.v1.admin.auth.password_reset import router as admin_password_reset_router

app = FastAPI(title="Google Developer Group on Campus, UNN Community API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://127.0.0.1:3000",
                 "http://localhost:5173",
                 "http://127.0.0.1:5173"],  
    allow_credentials=True,
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
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(events.router, prefix="/events", tags=["events"])
# app.include_router(projects.router, prefix="/projects", tags=["projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to the GDGoC, UNN Community API!"}