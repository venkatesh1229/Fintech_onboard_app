# ============================================================
# utils/hashing.py — Password Hashing with bcrypt
# ============================================================
# Never store plain text passwords. bcrypt adds a "salt"
# (random data) and hashes it, making brute-force attacks
# computationally expensive.
# ============================================================

from passlib.context import CryptContext

# Use bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password.
    
    Example:
        hash_password("MySecret123") 
        → "$2b$12$abcdefghij..." (60-char hash)
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare a plain text password against its stored hash.
    
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
