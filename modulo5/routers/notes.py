from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.note import CreateNote, NoteResponse
from models.db_models import Note
from dependencies import get_current_user
from database import get_db
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(Note).all()
    return db.query(Note).filter(Note.owner_id == current_user.id).all()

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: CreateNote, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/{id}", response_model=NoteResponse)
def get_note(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    if current_user.role != "admin" and note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver esta nota")
    return note

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    if current_user.role != "admin" and note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta nota")
    db.delete(note)
    db.commit()