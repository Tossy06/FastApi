from pydantic import BaseModel, Field

class CreateNote(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=10)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        from_attributes = True