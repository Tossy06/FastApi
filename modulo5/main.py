from fastapi import FastAPI
from database import engine
from models import db_models
from routers import auth, notes, products

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API con base de datos",
    description="Curso FastAPI — Módulo 5",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")