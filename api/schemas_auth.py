from core.config import CamelModel
from pydantic import BaseModel

class LoginRequest(CamelModel):
    email: str
    password: str

class RefreshRequest(CamelModel):
    refresh_token: str

class TokenResponse(CamelModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str | None = None
