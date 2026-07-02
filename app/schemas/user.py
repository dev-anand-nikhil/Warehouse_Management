from datetime import datetime
from pydantic import BaseModel
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
