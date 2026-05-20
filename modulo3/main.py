from fastapi import FastAPI
from routers import products, tasks

tags_metadata = [
    {
        "name": "Products",
        "description": "Operaciones con productos — crear, leer, actualizar y eliminar"
    },
    {
        "name": "Tasks",
        "description": "Gestión de tareas con prioridades"
    },
]

app = FastAPI(
    title= "Trabajos y productos",
    description="API de ejemplo Curso de FastAPI",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(products.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")