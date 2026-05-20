from pydantic import BaseModel, Field

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