from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks, files, gallery
from fastapi import Request
import time
import os
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from config import limiter
UPLOAD_DIR = "uploads"


app = FastAPI(
    title= "Module 6 CORS",
    description="Learn about CORS in FastApi",
    version="1.0.0"
)

# Registra el limiter en el estado de la app
app.state.limiter = limiter

# Registra el handler de error cuando se excede el límite
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

#==========================WEBSOCKETS================================
@app.websocket("/ws/chat")
async def websocket__enpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"ECHO: {data}")
    except WebSocketDisconnect:
        print("Cliente desconectado")

# WebSocket para verificar existencia de archivos
@app.websocket("/ws/gallery")
async def websocket_gallery(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Recibir mensaje con nombre de archivo
            filename = await websocket.receive_text()
            
            # Verificar si el archivo existe en uploads/
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                await websocket.send_text("Existe")
            else:
                await websocket.send_text("No existe")
                
    except WebSocketDisconnect:
        print(f"Cliente WebSocket desconectado")
    except Exception as e:
        print(f"Error en WebSocket: {str(e)}")
        await websocket.close()

app.include_router(tasks.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1")
app.include_router(gallery.router, prefix="/api/v1")

