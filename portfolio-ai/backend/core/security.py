from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from backend.core.config import settings

# Configure CryptContext to use secure bcrypt hashing mechanisms
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a raw, incoming password string against its stored hash value.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a secure, salted bcrypt hash from a raw password string.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Generates a cryptographically signed JSON Web Token (JWT) with an expiration timestamp.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # Inject the token expiration claim into payload dict
    to_encode.update({"exp": expire})
    
    # Encrypt the claims mapping using the global configuration variables
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt