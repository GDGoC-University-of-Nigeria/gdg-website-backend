from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.user import User
from app.core.security import hash_password
import logging

logger = logging.getLogger(__name__)

def create_user(db: Session, email: str, password: str, full_name: str | None, phone: str | None):
   
    try:
        # Validate email format
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        
        # Validate password
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check if email exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            logger.warning(f"Attempt to register with existing email: {email}")
            raise ValueError("Email already registered")

        # Hash password
        try:
            hashed_password = hash_password(password)
        except Exception as e:
            logger.error(f"Password hashing failed: {str(e)}")
            raise RuntimeError("Failed to process password")

        # Create user
        user = User(
            email=email,
            full_name=full_name,
            phone=phone,
            hashed_password=hashed_password,
            provider="local",
            provider_user_id=email
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Successfully created user with email: {email}")
        return user
        
    except ValueError:
        # Re-raise ValueError as-is (validation errors)
        db.rollback()
        raise
        
    except IntegrityError as e:
        # Handle database constraint violations
        db.rollback()
        logger.error(f"Database integrity error creating user: {str(e)}")
        
        # Check specific constraint violations
        if "unique constraint" in str(e).lower() and "email" in str(e).lower():
            raise ValueError("Email already registered")
        else:
            raise RuntimeError("Database constraint violation occurred")
    
    except SQLAlchemyError as e:
        # Handle other database errors
        db.rollback()
        logger.error(f"Database error creating user: {str(e)}")
        raise RuntimeError("Failed to create user due to database error")
    
    except Exception as e:
        # Handle unexpected errors
        db.rollback()
        logger.error(f"Unexpected error creating user: {str(e)}", exc_info=True)
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")