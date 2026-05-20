from fastapi import FastAPI, HTTPException, status
from models.tasks import ResponseTask, CreateTask
from typing import List, Optional

app = FastAPI()


tasks_db = {
    1: {"id": 1, "title": "Comprar mercado", "description": "Leche, huevos, pan", "priority": 2, "completed": False},
    2: {"id": 2, "title": "Estudiar FastAPI", "description": "Módulo 3 de Pydantic", "priority": 3, "completed": False},
    3: {"id": 3, "title": "Llamar al médico", "description": None, "priority": 1, "completed": True},
    4: {"id": 4, "title": "Hacer ejercicio", "description": "30 minutos de cardio", "priority": 2, "completed": True},
    5: {"id": 5, "title": "Leer un libro", "description": None, "priority": 1, "completed": False},
}

# Traer todas las tareas
@app.get("/tasks", response_model= List[ResponseTask])
def tasks(completed: Optional[bool] = None):
    if completed is None:
        return list(tasks_db.values())
    return[task for task in tasks_db.values() if task["completed"] == completed]

# Crear tareas
@app.post("/tasks", response_model= ResponseTask)
def create_task(task: CreateTask):
    new_id = max(tasks_db.keys()) + 1
    task_data = task.model_dump()
    task_data["id"] = new_id
    tasks_db[new_id] = task_data
    return task_data

# Obtener tareas por id
@app.get("/tasks/{id}", response_model= ResponseTask)
def task_by_id(id: int):
    if tasks_db.get(id) is None:
        raise HTTPException(
            status_code= 404,
            detail="Tarea no encontrada"
        )
    return tasks_db[id]

# Maracr tarea como completa
# No recibe body
@app.patch("/tasks/{id}/completed", response_model=ResponseTask)
def complete_task(id: int):
    if tasks_db.get(id) is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tasks_db[id]["completed"] = True
    return tasks_db[id]

# Eliminar tarea
@app.delete("/tasks/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_task(id:int):
    if tasks_db.pop(id, None) is None:
        raise HTTPException(
            status_code= 404,
            detail="Tarea no encontrada"
        )