"""Security utilities: password hashing and JWT handling."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import uuid
import hashlib

from passlib.context import CryptContext
import jwt  # PyJWT

from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# ----- Password Hashing -----

def hash_password(plain: str) -> str:
    # bcrypt underlying limit is mitigated by bcrypt_sha256 which hashes first with sha256
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ----- Refresh Token Opaque Generation -----

def generate_refresh_token() -> str:
    # Random UUID + time salt
    raw = f"{uuid.uuid4()}:{datetime.now(timezone.utc).timestamp()}"
    return hashlib.sha256(raw.encode()).hexdigest()

# ----- JWT (Access Token) -----

def create_access_token(subject: str, extra_claims: Dict[str, Any] | None = None, expires_minutes: int | None = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode: Dict[str, Any] = {"sub": subject}
    if extra_claims:
        to_encode.update(extra_claims)
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
