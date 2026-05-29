from fastapi import APIRouter, Request, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import time
from config import limiter

# Configuración para archivos
ALLOWED_TYPES = ["image/jpeg", "image/png"]
MAX_SIZE = 2 * 1024 * 1024
UPLOAD_DIR = "uploads"

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/gallery", tags=["Gallery"])

def image_render(filename: str, size_bytes: int):
    print(f"[TASK] Imagen procesada: {filename}")
    print(f"[LOG] Archivo subido: {filename} — {size_bytes} bytes")
    
    # Simula proceso lento
    time.sleep(1)
    
    print(f"[LOG] Procesamiento completo: {filename}")


@router.post("/upload")
@limiter.limit("5/minute")
async def upload(request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Validar tipo de archivo
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no permitido. Solo JPEG y PNG"
        )
    
    # Leer y validar tamaño
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Archivo muy grande, máximo 2MB")
    
    # Guardar el archivo físicamente
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Agregar tarea en background
    background_tasks.add_task(image_render, file.filename, len(contents))
    
    return {"filename": file.filename, "size_bytes": len(contents)}


@router.get("")
@limiter.limit("10/minute")
async def list_files(request: Request):
    """Lista todos los archivos en uploads/"""
    try:
        files = []
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                files.append(filename)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar archivos: {str(e)}")


@router.get("/{filename}")
@limiter.limit("10/minute")
async def download_file(request: Request, filename: str):
    """Descarga un archivo específico"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Verificar que sea un archivo (no directorio)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=400, detail="No es un archivo válido")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )