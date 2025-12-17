from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api import auth, users, events, projects
from app.core.config import settings

app = FastAPI(title="Google Developer Group on Campus, UNN Community API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Include API routes
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(events.router, prefix="/events", tags=["events"])
# app.include_router(projects.router, prefix="/projects", tags=["projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to the GDGoC, UNN Community API!"}