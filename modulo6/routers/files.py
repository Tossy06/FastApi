from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
import os
import time

router = APIRouter(prefix="/files", tags=["Files"])

ALLOWED_TYPES = ["image/jpeg", "image/png"]
MAX_SIZE = 2 * 1024 * 1024

def image_render(filename: str, size_bytes: int):

    print(f"[LOG] Archivo subido: {filename} — {size_bytes} bytes")

    # Simula proceso lento
    time.sleep(2)

    print(f"[LOG] Procesamiento completo: {filename}")

@router.post("/upload")
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code= 400,
            detail="Tipo de archivo no permitido"
        )
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Archivo muy grande, máximo 2MB")
    
    path = f"uploads/{file.filename}"
    with open(path, "wb") as buffer:
        buffer.write(contents)

    background_tasks.add_task(image_render,file.filename,len(contents))
        
    return {"filename": file.filename, "size_bytes": len(contents)}

@router.get("/download/{filename}")
def download(filename: str):
    path = f"uploads/{filename}"

    if not os.path.exists(path):
        raise HTTPException(
            status_code = 404,
            detail = "Archivo no encontrado"
        )
    return FileResponse(path)

@router.get("/stream/{filename}")
def stream(filename: str):
    path = f"uploads/{filename}"
    if not os.path.exists(path):
        raise HTTPException(
            status_code = 404,
            detail = "Archivo no encontrado"
        )
    
    def file_generator():
        with open(path, "rb") as f:
            yield from f  # envía el archivo en chunks
    
    return StreamingResponse(file_generator(), media_type="image/jpeg")
    
