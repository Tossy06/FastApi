from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks, files
from fastapi import Request
import time
import os

app = FastAPI(
    title= "Module 6 CORS",
    description="Learn about CORS in FastApi",
    version="1.0.0"
)

os.makedirs("uploads", exist_ok=True)

@app.middleware("http")
async def log_response(request: Request, call_next):
    # Tiempo en el que entro la resquest
    start = time.time()

    response = await call_next(request) # Pasa al endpoint o siguiente middleware

    # Calculamos la difrencia entre el timpo de entrada y el actual ( cuanto tardó)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} → {response.status_code} ({duration * 1000:.3f}ms)")

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # qué orígenes acepta
    allow_credentials=True,                   # permite cookies/auth headers
    allow_methods=["*"],                      # qué métodos HTTP acepta
    allow_headers=["*"],                      # qué headers acepta
)


app.include_router(tasks.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1")