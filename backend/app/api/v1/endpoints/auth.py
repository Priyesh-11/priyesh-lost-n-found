from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud.crud_user import user as crud_user
from app.services.auth_service import auth_service
from app.schemas.auth import (
    Token, 
    LoginRequest, 
    PasswordResetRequest, 
    PasswordResetConfirm,
    ResendVerificationRequest
)
from app.schemas.user import UserCreate, UserOut

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
    db: Session = Depends(deps.get_db),
    request: ResendVerificationRequest,
) -> Any:
    """Resend verification email"""
    try:
        auth_service.resend_verification_email(db, request.email)
        return {"message": "Verification email sent! Please check your inbox."}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

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
