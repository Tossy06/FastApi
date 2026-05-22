from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, status

#=================bcrypt==================
# Definimos el esquema con el que vamos a hacer el hash
# Y dejamos deprecated="auto", por si en un futuro cambaimos de esuqema sigan leyendo los del viejo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

#=================== JWT ==================================
# Usamos unas secret key para la signature
SECRET_KEY = "14862d6137a8de0b9910f4dc1eced20604f90dedbbd4af6c4b4962d4f07fcedd"
# Algoritmo que usaremos para la firma
ALGORITHM = "HS256"
# Expriración del token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta= None) -> str:
    to_encode = data.copy() # Este sera nuestro payload, no mutamos la data original
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    # Agregamos al payload la fecha de expiración
    to_encode["exp"] = expire

    # Retornamos el payload, la secret key con la que firmaremso y el algoritmo de firma
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado", headers={"WWW-Authenticate": "Bearer"})