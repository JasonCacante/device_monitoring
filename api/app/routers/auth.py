import random
import string
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])


def generate_otp() -> str:
    """Generate a 6-digit OTP code"""
    return "".join(random.choices(string.digits, k=6))


@router.post("/request-otp", response_model=dict)
async def request_otp(request: schemas.OTPRequest, db: Session = Depends(get_db)):
    """
    Request an OTP code for login.
    If user doesn't exist, create them with default role.
    """
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        # Create new user with default role
        # Auto-detect role based on email for demo purposes
        role = models.UserRole.STAFF
        if "admin" in request.email.lower():
            role = models.UserRole.ADMIN
        elif "customer" in request.email.lower():
            role = models.UserRole.CUSTOMER

        user = models.User(
            email=request.email, name=request.email.split("@")[0].title(), role=role
        )
        db.add(user)

    # Generate OTP
    otp_code = generate_otp()
    user.otp_code = otp_code
    user.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

    db.commit()

    # TODO: Send OTP via email service
    # For now, just log it to console
    print(f"\n{'=' * 50}")
    print(f"[OTP LOGIN] Email: {request.email}")
    print(f"[OTP LOGIN] Code: {otp_code}")
    print(f"[OTP LOGIN] Expires in 5 minutes")
    print(f"{'=' * 50}\n")

    return {
        "message": "OTP sent successfully",
        "email": request.email,
        "expires_in_minutes": 5,
        # Include OTP in response for development only
        "otp_code": otp_code,
    }


@router.post("/verify-otp", response_model=schemas.AuthResponse)
async def verify_otp(request: schemas.OTPVerify, db: Session = Depends(get_db)):
    """
    Verify OTP code and return access token
    """
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.otp_code or user.otp_code != request.otp_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP code"
        )

    if not user.otp_expires_at or datetime.now(timezone.utc) > user.otp_expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP code has expired"
        )

    # Clear OTP after successful verification
    user.otp_code = None
    user.otp_expires_at = None
    db.commit()

    # Generate JWT token
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )

    print(f"\n[AUTH SUCCESS] User {user.email} logged in as {user.role.value}\n")

    return schemas.AuthResponse(
        access_token=access_token, token_type="bearer", user=user
    )


@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get current authenticated user information"""
    return current_user


@router.post("/logout")
async def logout(current_user: models.User = Depends(auth.get_current_user)):
    """
    Logout current user.
    In JWT-based auth, client should delete the token.
    """
    return {"message": "Logged out successfully", "user": current_user.email}
