# ============================================================
# dependencies.py — FastAPI Shared Dependencies
# ============================================================
# These functions are injected into routes using Depends().
# They extract and validate the current user from the JWT
# token in the Authorization header.
# ============================================================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.auth import decode_access_token
from app.storage import get_user_by_email, get_admin_by_email

# Tell FastAPI where to find the token (the /api/auth/login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Validate merchant JWT token and return the current merchant."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None or role != "merchant":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


def get_current_admin(token: str = Depends(oauth2_scheme)) -> dict:
    """Validate admin JWT token and return the current admin."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin access required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None or role != "admin":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    admin = get_admin_by_email(email)
    if admin is None:
        raise credentials_exception

    return admin
