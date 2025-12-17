"""
Database session management for the GDGoC UNN API.

This module configures the SQLAlchemy database engine and session factory,
providing database connections for the FastAPI application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create database engine using the DATABASE_URL from configuration
# echo=True enables SQL query logging for debugging
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# SessionLocal is a factory for creating database sessions
# autocommit=False: Transactions must be explicitly committed
# autoflush=False: Changes are not automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session to route handlers.
    
    Yields:
        Session: A SQLAlchemy database session
        
    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()