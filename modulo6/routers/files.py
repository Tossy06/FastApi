from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil

router = APIRouter(prefix="/files", tags=["Files"])

ALLOWED_TYPES = ["image/jpeg", "image/png"]
MAX_SIZE = 2 * 1024 * 1024

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
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
        
    return {"filename": file.filename, "size_bytes": len(contents)}


