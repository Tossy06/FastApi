from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str