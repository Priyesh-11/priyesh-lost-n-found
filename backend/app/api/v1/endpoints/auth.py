from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud.crud_user import user as crud_user
from app.services.auth_service import auth_service
from app.services.email_service import email_service
from app.schemas.auth import (
    Token, 
    LoginRequest, 
    PasswordResetRequest, 
    PasswordResetConfirm,
    ResendVerificationRequest
)
from app.schemas.user import UserCreate, UserOut
from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Login with email and password"""
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    elif not user.is_verified:
        raise HTTPException(
            status_code=403, 
            detail="Please verify your email address before logging in. Check your inbox for the verification link."
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.post("/register", response_model=dict)
def register_user(
    *,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register new user
    """
    import logging
    from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError
    
    logger = logging.getLogger(__name__)
    
    try:
        user = auth_service.register_user(db=db, user_in=user_in)
    except ValueError as e:
        # Business logic errors (email/username already exists)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as e:
        # Database constraint violations (duplicate email/username)
        logger.error(f"Database integrity error during registration: {str(e)}")
        db.rollback()
        
        # Check if it's a duplicate email or username
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        if 'email' in error_msg.lower() or 'duplicate' in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        elif 'username' in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed. Please check your information and try again."
            )
    except (OperationalError, DatabaseError) as e:
        # Database connection or operational errors
        logger.error(f"Database error during registration: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service temporarily unavailable. Please try again later."
        )
    except Exception as e:
        # Catch all other exceptions
        logger.error(f"Unexpected error during registration: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration. Please try again."
        )
    
    # Queue verification email in the background so the API response returns immediately
    if user.verification_token:
        # Capture values before background task to avoid closure issues
        user_email = user.email
        user_token = user.verification_token
        user_username = user.username
        
        def send_email_with_error_handling():
            """Wrapper to handle email sending errors in background task"""
            try:
                logger.info(f"📧 Background task started: Sending verification email to {user_email}")
                email_service.send_verification_email(
                    email_to=user_email,
                    token=user_token,
                    username=user_username
                )
                logger.info(f"✅ Verification email sent successfully to {user_email}")
            except Exception as e:
                logger.error(f"❌ Failed to send verification email to {user_email}: {type(e).__name__}: {str(e)}", exc_info=True)
                # Don't raise - background task errors shouldn't affect the response
        
        background_tasks.add_task(send_email_with_error_handling)
        logger.info(f"📧 Verification email task queued for {user_email} (token: {user_token[:10]}...)")

    # Return success message WITHOUT tokens - user must verify email first
    return {
        "message": "Registration successful! Please check your email to verify your account before logging in.",
        "email": user.email,
        "username": user.username
    }

@router.post("/verify-email/{token}")
def verify_email(
    token: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Verify user email with token from email link"""
    try:
        user = auth_service.verify_email(db, token)
        return {
            "message": "Email verified successfully!",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_verified": user.is_verified
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/resend-verification")
def resend_verification(
    *,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    request: ResendVerificationRequest,
) -> Any:
    """Resend verification email"""
    try:
        user = auth_service.resend_verification_email(db, request.email)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
    if user.verification_token:
        # Capture values before background task to avoid closure issues
        user_email = user.email
        user_token = user.verification_token
        user_username = user.username
        
        def send_email_with_error_handling():
            """Wrapper to handle email sending errors in background task"""
            try:
                logger.info(f"📧 Background task started: Resending verification email to {user_email}")
                email_service.send_verification_email(
                    email_to=user_email,
                    token=user_token,
                    username=user_username
                )
                logger.info(f"✅ Resend verification email sent successfully to {user_email}")
            except Exception as e:
                logger.error(f"❌ Failed to resend verification email to {user_email}: {type(e).__name__}: {str(e)}", exc_info=True)
        
        background_tasks.add_task(send_email_with_error_handling)
        logger.info(f"📧 Resend verification email task queued for {user_email} (token: {user_token[:10]}...)")
    
    return {"message": "Verification email sent! Please check your inbox."}

@router.post("/forgot-password")
def forgot_password(
    *,
    db: Session = Depends(deps.get_db),
    request: PasswordResetRequest,
) -> Any:
    """Request password reset email"""
    auth_service.request_password_reset(db, request.email)
    # Always return success to prevent email enumeration
    return {"message": "If your email is registered, you will receive a password reset link."}

@router.post("/reset-password")
def reset_password(
    *,
    db: Session = Depends(deps.get_db),
    request: PasswordResetConfirm,
) -> Any:
    """Reset password with token"""
    try:
        user = auth_service.reset_password(db, request.token, request.new_password)
        return {
            "message": "Password reset successful! You can now login with your new password.",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/test-email")
def test_email(
    *,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Test endpoint to verify email sending (requires authentication)"""
    from app.core.config import settings
    
    # Check if SMTP is configured
    smtp_status = {
        "SMTP_HOST": settings.SMTP_HOST or "NOT SET",
        "SMTP_PORT": settings.SMTP_PORT or 587,
        "SMTP_USER": settings.SMTP_USER or "NOT SET",
        "SMTP_PASSWORD": "SET" if settings.SMTP_PASSWORD else "NOT SET",
        "FRONTEND_URL": settings.FRONTEND_URL,
    }
    
    # Try to send a test email
    try:
        email_service.send_verification_email(
            email_to=current_user.email,
            token="test-token-12345",
            username=current_user.username
        )
        return {
            "status": "success",
            "message": f"Test email sent to {current_user.email}. Check your inbox!",
            "smtp_config": smtp_status
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send test email: {str(e)}",
            "smtp_config": smtp_status,
            "error_type": type(e).__name__
        }
