# ============================================================
# dependencies.py — FastAPI Shared Dependencies
# ============================================================
# These functions are injected into routes using Depends().
# They extract and validate the current user from the JWT
# token in the Authorization header.
# ============================================================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db
from app.auth import decode_access_token
from app import models

# Tell FastAPI where to find the token (the /api/auth/login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Extract and validate the current merchant user from the JWT token.
    Raises 401 if token is missing, expired, or invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        role:  str = payload.get("role")

        # Ensure this is a merchant token, not an admin token
        if email is None or role != "merchant":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Look up the user in the database
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.AdminUser:
    """
    Same as get_current_user but validates admin role.
    Used to protect all /api/admin/* endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin access required",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        role:  str = payload.get("role")

        if email is None or role != "admin":
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    admin = db.query(models.AdminUser).filter(models.AdminUser.email == email).first()
    if admin is None:
        raise credentials_exception

    return admin
