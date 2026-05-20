from fastapi import APIRouter, HTTPException, status, Depends
from models.note import CreateNote, NoteResponse
from dependencies import get_current_user, get_current_admin
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"])

notes_db = {}

@router.get("", response_model=List[NoteResponse])
def get_notes(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "admin":
        return list(notes_db.values())
    
    return [
        note for note in notes_db.values()
        if note["owner"] == current_user["email"]
    ]

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: CreateNote, current_user: dict = Depends(get_current_user)):

    new_id = max(notes_db.keys(), default=0) + 1
    note_data = note.model_dump()
    note_data["id"] = new_id
    note_data["owner"] = current_user["email"]
    notes_db[new_id] = note_data
    return note_data

@router.get("/{id}", response_model=NoteResponse)
def get_note(id: int, current_user: dict = Depends(get_current_user)):

    note = notes_db.get(id)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    if current_user["role"] == "admin":
        return note
    
    if note["owner"] == current_user["email"]:
        return note
    
    raise HTTPException(
        status_code=403,
        detail="No tienes permisos para ver esta nota"
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, current_user: dict = Depends(get_current_user)):

    note = notes_db.get(id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Nota no encontrada"
        )
    
    if current_user["role"] == "admin":
        notes_db.pop(id)
        return
    
    if note["owner"] == current_user["email"]:
        notes_db.pop(id)
        return
    
    raise HTTPException(
        status_code=403,
        detail="No tienes permisos para eliminar esta nota"
    )