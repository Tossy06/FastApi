from fastapi import APIRouter, Request
from config import limiter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("")
@limiter.limit("3/minute")
def get_tasks(request: Request):
    # Por ahora estará hasrcodeada
    return [
        {"id": 1, "title": "Aprender FastAPI", "done": False},
        {"id": 2, "title": "Crear API REST", "done": True},
        {"id": 3, "title": "Desplegar proyecto en AWS", "done": False},
    ]