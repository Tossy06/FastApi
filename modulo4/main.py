from fastapi import FastAPI
from routers import auth, notes

tags_metadata = [
    {"name": "Auth", "description": "Registro, login y perfil"},
    {"name": "Notes", "description": "Notas personales — requieren autenticación"},
]

app = FastAPI(
    title="API con autenticación",
    description="Curso FastAPI — Módulo 4",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")