from fastapi import APIRouter, status, HTTPException, Depends
from models.user import UserCreate, UserResponse, Token
from fastapi.security import OAuth2PasswordRequestForm
from security import hash_password, verify_password, create_access_token
from database import users_db

router = APIRouter(prefix="/auth", tags=["Auth"])

# Registro
@router.post("/register", response_model= UserResponse, status_code= status.HTTP_201_CREATED)
def register(user: UserCreate):
    for item in users_db:
        if item["email"] == user.email:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Email ya registrado"
            )
    hashed_password = hash_password(user.password)

    new_user = {
        "id": (max((item["id"] for item in users_db), default=0)) + 1,
        "email": user.email,
        "password": hashed_password
    }

    users_db.append(new_user)

    return new_user


# Logun
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = None

    # Buscar usuario por email
    for item in users_db:
        if item["email"] == form_data.username:
            user = item
            break

    # Usuario no encontrado
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Verificar contraseña
    if not verify_password(
        form_data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Crear JWT
    access_token = create_access_token(
        {
            "sub": user["email"]
        }
    )

    # Responder con el token
    return Token(
        access_token=access_token,
        token_type="bearer"
    )