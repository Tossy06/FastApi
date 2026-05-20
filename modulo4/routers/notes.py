from fastapi import APIRouter, HTTPException, status, Depends
from models.note import CreateNote, NoteResponse
from dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"], dependencies=[Depends(get_current_user)])

notes_db = {}

@router.get("", response_model=List[NoteResponse])
def get_notes():
    return list(notes_db.values())

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: CreateNote):
    new_id = max(notes_db.keys(), default=0) + 1
    note_data = note.model_dump()
    note_data["id"] = new_id
    notes_db[new_id] = note_data
    return note_data

@router.get("/{id}", response_model=NoteResponse)
def get_note(id: int):
    if notes_db.get(id) is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return notes_db[id]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int):
    if notes_db.pop(id, None) is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")