# ============================================================
# routes/auth_routes.py — Authentication Endpoints
# ============================================================
# POST /api/auth/register  → Merchant registration
# POST /api/auth/login     → Merchant login → returns JWT
# POST /api/auth/admin/login → Admin login → returns JWT
# ============================================================

from fastapi import APIRouter, HTTPException, status
from app import schemas
from app.storage import get_user_by_email, get_user_by_mobile, get_admin_by_email, create_user
from app.utils.hashing import hash_password, verify_password
from app.auth import create_access_token

router = APIRouter()


# ============================================================
# MERCHANT REGISTRATION
# POST /api/auth/register
# ============================================================
@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register_merchant(user_data: schemas.UserCreate):
    """
    Create a new merchant account.
    """
    if get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if get_user_by_mobile(user_data.mobile):
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    hashed_pw = hash_password(user_data.password)
    user = create_user({
        "business_name": user_data.business_name,
        "contact_person": user_data.contact_person,
        "mobile": user_data.mobile,
        "email": user_data.email,
        "business_type": user_data.business_type,
        "pan_number": user_data.pan_number,
        "gst_number": user_data.gst_number,
        "services": user_data.services,
        "hashed_password": hashed_pw,
    })

    return user


# ============================================================
# MERCHANT LOGIN
# POST /api/auth/login
# ============================================================
@router.post("/login", response_model=schemas.TokenResponse)
def login_merchant(credentials: schemas.LoginRequest):
    """
    Authenticate a merchant and return a JWT access token.
    """
    user = get_user_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": user["email"], "role": "merchant"})
    return {"access_token": token, "token_type": "bearer", "role": "merchant"}


# ============================================================
# ADMIN LOGIN
# POST /api/auth/admin/login
# ============================================================
@router.post("/admin/login", response_model=schemas.TokenResponse)
def login_admin(credentials: schemas.LoginRequest):
    """
    Authenticate an admin user and return a JWT with role="admin".
    """
    admin = get_admin_by_email(credentials.email)

    if not admin or not verify_password(credentials.password, admin["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )

    token = create_access_token({"sub": admin["email"], "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "role": "admin"}
