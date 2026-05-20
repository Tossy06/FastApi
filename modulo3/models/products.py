from pydantic import BaseModel, Field
from typing import Optional

class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=3, max_length=50)
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    categoria: Optional[str] = Field(default=None, max_length=30)

class ProductoRespuesta(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    categoria: Optional[str] = None

class ProductoActualizar(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=50)
    precio: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    categoria: Optional[str] = Field(default=None, max_length=30)
