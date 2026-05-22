from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.product import CreateProduct, ProductResponse, UpdateProduct
from models.db_models import Products
from dependencies import get_current_user, get_current_admin
from database import get_db
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.get("", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Products).all()
    return products

@router.get("/{id}", response_model = ProductResponse)
def ge_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == id).first()

    if product is None:
        raise HTTPException(
            status_code= 404,
            detail= "Producto no encontrado"
        )
    return product

@router.post("", response_model = ProductResponse, status_code = status.HTTP_201_CREATED)
def create_product(product: CreateProduct, db: Session = Depends(get_db), _= Depends(get_current_admin)):
    new_product = Products(
        name = product.name,
        price = product.price,
        stock = product.stock,
        category = product.category
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{id}", response_model=ProductResponse)
def update_all(
    id: int,
    product: CreateProduct,
    db: Session = Depends(get_db),
    _ = Depends(get_current_admin)
):
    updated_product = db.query(Products).filter(Products.id == id).first()

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    for key, value in product.model_dump().items():
        setattr(updated_product, key, value)

    db.commit()
    db.refresh(updated_product)

    return updated_product


@router.patch("/{id}", response_model= ProductResponse)
def update_any(id: int, product: UpdateProduct, db: Session = Depends(get_db), _= Depends(get_current_admin)):
    # Primero validamos que el producto exista
    product_changes = db.query(Products).filter(Products.id == id).first()

    if product_changes is None:
        raise HTTPException(
            status_code= 404,
            detail= "Producto no encontrado"
        )
    # Los cambios vienen como objeto pydantic en el parametro product
    # así que lo convertimos nuevamente a diccionario
    changes = product.model_dump(exclude_unset=True).items()

    # items() devuelve pares (key, value)
    for key, value in changes:
        # setattr(objeto, atributo, valor)
        setattr(product_changes, key, value)

    db.commit()
    db.refresh(product_changes)

    return product_changes

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db),_= Depends(get_current_admin)):
    product_delete = db.query(Products).filter(Products.id == id).first()
    if product_delete is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(product_delete)
        


