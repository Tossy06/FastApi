from pydantic import BaseModel, Field
from typing import Optional

class CreateTask(BaseModel):
    title: str = Field(min_length= 3, max_length= 100)
    description: Optional[str] = Field(default= None,  max_length= 300)
    priority: int = Field(ge=1, le= 3)
    completed: bool = Field(default= False)

class ResponseTask(BaseModel):
    id: int
    title: str 
    description: Optional[str] = None
    priority: int 
    completed: bool
