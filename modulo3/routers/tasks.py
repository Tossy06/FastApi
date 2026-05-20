from fastapi import APIRouter, HTTPException, status, Depends
from models.task import ResponseTask, CreateTask
from typing import List, Optional

router = APIRouter(prefix="/tasks", tags=["Tasks"])


tasks_db = {
    1: {"id": 1, "title": "Comprar mercado", "description": "Leche, huevos, pan", "priority": 2, "completed": False},
    2: {"id": 2, "title": "Estudiar FastAPI", "description": "Módulo 3 de Pydantic", "priority": 3, "completed": False},
    3: {"id": 3, "title": "Llamar al médico", "description": None, "priority": 1, "completed": True},
    4: {"id": 4, "title": "Hacer ejercicio", "description": "30 minutos de cardio", "priority": 2, "completed": True},
    5: {"id": 5, "title": "Leer un libro", "description": None, "priority": 1, "completed": False},
}

# Validacion de tareas existente
def get_task_or_404(id: int):
    if tasks_db.get(id, None) is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tasks_db[id] 

# Traer todas las tareas
@router.get("", response_model= List[ResponseTask])
def tasks(completed: Optional[bool] = None):
    if completed is None:
        return list(tasks_db.values())
    return[task for task in tasks_db.values() if task["completed"] == completed]

# Crear tareas
@router.post("", response_model= ResponseTask, status_code= status.HTTP_201_CREATED)
def create_task(task: CreateTask):
    new_id = max(tasks_db.keys()) + 1
    task_data = task.model_dump()
    task_data["id"] = new_id
    tasks_db[new_id] = task_data
    return task_data

# Obtener tareas por id
@router.get("/{id}", response_model= ResponseTask)
def task_by_id(task = Depends(get_task_or_404)):
    return task

# Maracr tarea como completa
# No recibe body
@router.patch("/{id}/completed", response_model=ResponseTask)
def complete_task(task = Depends(get_task_or_404)):
    task["completed"] = True
    return task

# Eliminar tarea
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_task(id: int, _: dict = Depends(get_task_or_404)):
    tasks_db.pop(id)