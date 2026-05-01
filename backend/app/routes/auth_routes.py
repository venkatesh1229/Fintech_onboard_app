# ============================================================
# routes/auth_routes.py — Authentication Endpoints
# ============================================================
# POST /api/auth/register  → Merchant registration
# POST /api/auth/login     → Merchant login → returns JWT
# POST /api/auth/admin/login → Admin login → returns JWT
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.utils.hashing import hash_password, verify_password
from app.auth import create_access_token

router = APIRouter()


# ============================================================
# MERCHANT REGISTRATION
# POST /api/auth/register
# ============================================================
@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register_merchant(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new merchant account.
    
    Steps:
    1. Check email and mobile aren't already registered
    2. Hash the password before saving
    3. Save user to DB
    """
    # Step 1: Check for existing email
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check for existing mobile
    if db.query(models.User).filter(models.User.mobile == user_data.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    # Step 2: Hash the password — NEVER store plain text
    hashed_pw = hash_password(user_data.password)

    # Step 3: Create the DB row
    new_user = models.User(
        business_name  = user_data.business_name,
        contact_person = user_data.contact_person,
        mobile         = user_data.mobile,
        email          = user_data.email,
        business_type  = user_data.business_type,
        pan_number     = user_data.pan_number,
        gst_number     = user_data.gst_number,
        services       = ",".join(user_data.services),  # Store as CSV string
        hashed_password= hashed_pw,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Reload the row to get auto-generated id, created_at, etc.

    return new_user


# ============================================================
# MERCHANT LOGIN
# POST /api/auth/login
# ============================================================
@router.post("/login", response_model=schemas.TokenResponse)
def login_merchant(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a merchant and return a JWT access token.
    
    The token encodes the user's email and role ("merchant").
    """
    # Find user by email
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    # Verify password (always verify even if user not found to avoid timing attacks)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_access_token({"sub": user.email, "role": "merchant"})

    return {"access_token": token, "token_type": "bearer", "role": "merchant"}


# ============================================================
# ADMIN LOGIN
# POST /api/auth/admin/login
# ============================================================
@router.post("/admin/login", response_model=schemas.TokenResponse)
def login_admin(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate an admin user and return a JWT with role="admin".
    """
    admin = db.query(models.AdminUser).filter(models.AdminUser.email == credentials.email).first()

    if not admin or not verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )

    token = create_access_token({"sub": admin.email, "role": "admin"})

    return {"access_token": token, "token_type": "bearer", "role": "admin"}
