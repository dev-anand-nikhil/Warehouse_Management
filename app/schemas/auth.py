from pydantic import BaseModel
from app.models.user import UserRole

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(LoginRequest):
    role: UserRole
