import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import generate_verification_token
from app.crud.crud_user import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.email import send_password_reset_email

logger = logging.getLogger(__name__)

class AuthService:
    def register_user(self, db: Session, user_in: UserCreate) -> User:
        """Register a new user and send verification email"""
        try:
            # Check if user exists
            if crud_user.get_by_email(db, email=user_in.email):
                raise ValueError("Email already registered")
            if crud_user.get_by_username(db, username=user_in.username):
                raise ValueError("Username already taken")
            
            # Create user
            user = crud_user.create(db, obj_in=user_in)
            
            # Generate verification token
            token = generate_verification_token()
            user.verification_token = token
            db.add(user)
            db.commit()
            db.refresh(user)
            
            return user
        except ValueError:
            # Re-raise business logic errors
            raise
        except Exception as e:
            # Rollback on any other error
            db.rollback()
            logger.error(f"Error during user registration: {type(e).__name__}: {str(e)}", exc_info=True)
            raise
    
    def verify_email(self, db: Session, token: str) -> User:
        """Verify user email with token"""
        user = db.query(User).filter(User.verification_token == token).first()
        if not user:
            raise ValueError("Invalid or expired verification token")
        
        user.is_verified = True
        user.verification_token = None
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    def resend_verification_email(self, db: Session, email: str) -> None:
        """Resend verification email to user"""
        user = crud_user.get_by_email(db, email=email)
        if not user:
            raise ValueError("User not found")
        
        if user.is_verified:
            raise ValueError("Email already verified")
        
        # Generate new verification token
        token = generate_verification_token()
        user.verification_token = token
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    def request_password_reset(self, db: Session, email: str) -> None:
        """Generate password reset token and send email"""
        user = crud_user.get_by_email(db, email=email)
        if not user:
            # Don't reveal if email exists or not
            return
        
        # Generate reset token
        token = generate_verification_token()
        user.reset_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.add(user)
        db.commit()
        
        # Send password reset email
        try:
            send_password_reset_email(user.email, token)
        except Exception as e:
            logger.error(f"Failed to send password reset email: {str(e)}")
    
    def reset_password(self, db: Session, token: str, new_password: str) -> User:
        """Reset user password with token"""
        user = db.query(User).filter(User.reset_token == token).first()
        if not user:
            raise ValueError("Invalid or expired reset token")
        
        if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
            raise ValueError("Reset token has expired")
        
        # Update password
        from app.schemas.user import UserUpdate
        user_update = UserUpdate(password=new_password)
        user = crud_user.update(db, db_obj=user, obj_in=user_update)
        
        # Clear reset token
        user.reset_token = None
        user.reset_token_expires = None
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user

auth_service = AuthService()
