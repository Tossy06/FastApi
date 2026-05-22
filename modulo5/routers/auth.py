from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.user import UserRegister, UserResponse, UserUpdate
from models.db_models import User
from dependencies import get_current_user, get_current_admin
from security import hash_password, verify_password, create_access_token
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role="user",
        active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas", headers={"WWW-Authenticate": "Bearer"})
    token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/{id}", response_model= UserResponse)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db), _= Depends(get_current_admin)):
    user_update = db.query(User).filter(User.id == id).first()

    if user_update is None:
        raise HTTPException(
            status_code=404,
            detail = "El usuario no existe"
        ) 
    
    #Convertimos en diccionario
    # Y con items devolvemos pares (key, values)
    changes =  user.model_dump(exclude_unset = True).items()

    # Recorremos y asigamos los cambios al objeto con setattr
    for key, value in changes:
        #objeto.key = value
        setattr(user_update, key, value)
    db.commit()
    db.refresh(user_update)

    return user_update