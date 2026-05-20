from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from security import decode_token
from security import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

users_db = {}  # temporal — en módulo 5 esto será una DB real

users_db["admin@email.com"] = {
    "email": "admin@email.com",
    "password_hash": hash_password("admin1234"),
    "role": "admin",
    "active": True
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    email = decode_token(token)
    user = users_db.get(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    if not user["active"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    return user

def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user