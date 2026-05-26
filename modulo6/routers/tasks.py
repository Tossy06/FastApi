from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("")
def get_tasks():
    # Por ahora estará hasrcodeada
    return [
        {"id": 1, "title": "Aprender FastAPI", "done": False},
        {"id": 2, "title": "Crear API REST", "done": True},
        {"id": 3, "title": "Desplegar proyecto en AWS", "done": False},
    ]