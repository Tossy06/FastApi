from pydantic import BaseModel, Field
from typing import Optional

class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=8)

class UserDb(BaseModel):
    email: str
    password_hash: str
    role: str = "user"
    active: bool = True

class UserResponse(BaseModel):
    email: str
    role: str
    active: bool

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None

    class Config:
        from_attributes = True