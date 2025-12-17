# GDGoC UNN API

**Official Backend API for Google Developer Group on Campus, University of Nigeria, Nsukka**

This is the backend API for the GDGoC UNN community website, built with FastAPI. The platform serves as the central hub where students of the University of Nigeria, Nsukka can register as community members, participate in tech events, collaborate on open-source projects, and share their knowledge through blog posts.

---

## 🎯 Project Overview

### What is GDGoC UNN?

Google Developer Group on Campus (GDGoC) UNN is a student-led tech community at the University of Nigeria, Nsukka. The community focuses on:

- **Learning**: Organizing workshops, study sessions, and tech talks
- **Building**: Collaborating on open-source projects and hackathons
- **Sharing**: Publishing technical blog posts and tutorials
- **Networking**: Connecting students with similar interests and industry professionals

### Platform Features

This API powers a comprehensive community platform with the following features:

#### 👥 User Management
- **Google OAuth Authentication**: Secure login using university Google accounts
- **Profile Management**: Users can complete profiles with skills, GitHub links, and roles
- **Member Directory**: Browse and connect with other community members

#### 📅 Event Management
- **Event Creation**: Organizers can create and manage community events
- **Event Registration**: Members can register for workshops, meetups, and hackathons
- **Speaker Profiles**: Showcase guest speakers and their expertise
- **Event Calendar**: View upcoming and past community events

#### 🚀 Project Collaboration
- **Project Showcase**: Display ongoing and completed community projects
- **Contributor Applications**: Members can apply to contribute to projects
- **Role-based Collaboration**: Apply for specific roles (Frontend, Backend, Design, etc.)
- **Project Tracking**: Monitor project status and progress

#### ✍️ Blog Platform
- **Content Creation**: Members can write and publish technical blog posts
- **Markdown Support**: Rich text formatting for tutorials and articles
- **Content Moderation**: Admin verification before posts go live
- **Topic Categories**: Organize posts by niche (Web Dev, AI/ML, DevOps, etc.)

---

## 🏗️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast Python web framework
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Robust relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- **Authentication**: Google OAuth 2.0 - Secure authentication via Google
- **Python Version**: 3.11+

---

## 📊 Database Models

The API uses the following database models:

### User
Represents community members with OAuth authentication and profile information.
- Fields: email, provider, full_name, role, github, avatar_url, skills, profile_complete, is_active

### Event
Community events like workshops, meetups, and hackathons.
- Fields: title, description, image_url, date, start_time, end_time, location, creator_id

### Project
Open-source projects and collaborative initiatives.
- Fields: title, description, duration, start_date, end_date, github_repo, demo_video_url, status

### BlogPost
Technical articles and tutorials written by community members.
- Fields: title, image_url, content, content_format, is_verified, niche, author_id

### Speaker
Guest speakers and presenters at events.
- Fields: name, bio, image_url, topic, niche, event_id

### Applicant
Project collaboration applications and contributor approvals.
- Fields: user_id, project_id, role, is_contributor

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 14 or higher** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - [Download Git](https://git-scm.com/downloads/)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gdg/backend
   ```

2. **Create and activate a virtual environment**
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   
   Create a new PostgreSQL database:
   ```sql
   CREATE DATABASE gdgoc_unn;
   CREATE USER gdgoc_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE gdgoc_unn TO gdgoc_user;
   ```

5. **Configure environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update the following variables:
   ```env
   DATABASE_URL=postgresql+asyncpg://gdgoc_user:your_password@localhost/gdgoc_unn
   SECRET_KEY=your_secret_key_here_generate_a_strong_random_string
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   
   **Important**: Generate a secure `SECRET_KEY` using:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

---

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Interactive API explorer with request/response examples
  - Test endpoints directly from the browser

- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
  - Alternative documentation with a clean, readable interface

---

## 🛠️ Development Workflow

### Creating New Models

1. **Define the model** in `app/models/<model_name>.py`:
   ```python
   from sqlalchemy import Column, String
   from app.db.base import Base
   import uuid
   
   class MyModel(Base):
       __tablename__ = "my_models"
       id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
       name = Column(String, nullable=False)
   ```

2. **Import the model** in `app/db/base.py` to ensure it's discovered by Alembic

3. **Create a migration**:
   ```bash
   alembic revision --autogenerate -m "Add MyModel table"
   ```

4. **Review the migration** in `alembic/versions/` and apply it:
   ```bash
   alembic upgrade head
   ```

### Creating Pydantic Schemas

Define request/response schemas in `app/schemas/<schema_name>.py`:

```python
from pydantic import BaseModel
from uuid import UUID

class MyModelCreate(BaseModel):
    name: str

class MyModelRead(MyModelCreate):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
```

### Adding API Endpoints

1. **Create a router** in `app/api/<endpoint_name>.py`:
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   from app.db.session import get_db
   
   router = APIRouter()
   
   @router.get("/my-endpoint")
   async def get_items(db: Session = Depends(get_db)):
       return {"message": "Hello World"}
   ```

2. **Include the router** in `app/main.py`:
   ```python
   from app.api import my_endpoint
   
   app.include_router(my_endpoint.router, prefix="/api/my-endpoint", tags=["My Endpoint"])
   ```

### Database Migrations

- **Create a new migration**:
  ```bash
  alembic revision --autogenerate -m "Description of changes"
  ```

- **Apply migrations**:
  ```bash
  alembic upgrade head
  ```

- **Rollback last migration**:
  ```bash
  alembic downgrade -1
  ```

- **View migration history**:
  ```bash
  alembic history
  ```

### Code Quality

The project uses the following tools for code quality:

- **Ruff**: Fast Python linter and formatter
  ```bash
  ruff check .
  ruff format .
  ```

- **MyPy**: Static type checker
  ```bash
  mypy app
  ```

- **Pre-commit hooks**: Automatically run checks before commits
  ```bash
  pre-commit install
  pre-commit run --all-files
  ```

---

## 🧪 Testing

Run tests using pytest:

```bash
pytest
pytest -v  # Verbose output
pytest --cov=app  # With coverage report
```

---

## 📁 Project Structure

```
backend/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   └── env.py                  # Alembic configuration
├── app/
│   ├── api/                    # API route handlers
│   ├── core/                   # Core configuration
│   │   └── config.py           # Settings and environment variables
│   ├── crud/                   # Database operations
│   ├── db/                     # Database configuration
│   │   ├── base.py             # Base model class
│   │   └── session.py          # Database session management
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py             # User model
│   │   ├── event.py            # Event model
│   │   ├── project.py          # Project model
│   │   ├── blogpost.py         # BlogPost model
│   │   ├── speaker.py          # Speaker model
│   │   └── applicant.py        # Applicant model
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py             # User schemas
│   │   ├── event.py            # Event schemas
│   │   ├── project.py          # Project schemas
│   │   ├── blogpost.py         # BlogPost schemas
│   │   ├── speaker.py          # Speaker schemas
│   │   ├── applicant.py        # Applicant schemas
│   │   └── auth.py             # Authentication schemas
│   ├── services/               # Business logic
│   ├── deps.py                 # Dependency injection
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Test files
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🤝 Contributing

We welcome contributions from all GDGoC UNN members! Here's how you can contribute:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests if applicable
4. **Run code quality checks**: `ruff check . && mypy app`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and write clear commit messages

---

## 📝 License

This project is developed for the GDGoC UNN community.

---

## 📧 Contact

For questions or support, reach out to the GDGoC UNN team:

- **Community Website**: [Coming Soon]
- **Email**: gdgoc.unn@gmail.com
- **GitHub**: [GDGoC UNN Organization]

---

## 🙏 Acknowledgments

- Google Developer Groups for supporting campus communities
- University of Nigeria, Nsukka for hosting the community
- All GDGoC UNN members and contributors

---

**Built with ❤️ by the GDGoC UNN Community**