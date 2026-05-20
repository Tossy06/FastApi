from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from models.user import UserRegister, UserResponse
from dependencies import get_current_user, users_db
from security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    
    users_db[user.email] = {
        "email": user.email,
        "password_hash": hash_password(user.password),
        "role": "user",
        "active": True
    }
    return users_db[user.email]

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    
    if user is None or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = create_access_token(data={"sub": user["email"]})
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
def me(current_user: dict = Depends(get_current_user)):
    return current_user