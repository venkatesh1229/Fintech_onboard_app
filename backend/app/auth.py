# ============================================================
# auth.py — JWT Token Creation & Verification
# ============================================================
# Handles generating and decoding JWT tokens used for
# authenticating both merchants and admins.
# ============================================================

from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings


def create_access_token(data: dict) -> str:
    """
    Create a signed JWT token.
    
    Args:
        data: Payload to encode (usually {"sub": email, "role": "merchant"})
    
    Returns:
        A signed JWT string
    """
    to_encode = data.copy()

    # Set token expiry time
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Sign and return the token
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT token.
    
    Args:
        token: The JWT string from Authorization header
    
    Returns:
        The decoded payload dict, or raises JWTError if invalid/expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise  # Let the dependency handler catch this
