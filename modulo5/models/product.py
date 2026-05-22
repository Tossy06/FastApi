from pydantic import BaseModel, Field
from typing import Optional

class CreateProduct(BaseModel):
    name: str = Field(min_length = 3, max_length = 50)
    price: float = Field(gt = 0)
    stock: int = Field(ge = 0, default = 0)
    category: Optional[str] = Field(max_length = 30)

class UpdateProduct(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    price: Optional[float] = Field(default=None, ge=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = Field(default=None, max_length=30)

class ProductResponse(BaseModel):
    id: int
    name: str 
    price: float 
    stock: int 
    category: Optional[str] = None

    class Config:
        from_attributes = True