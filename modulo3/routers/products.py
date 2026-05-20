from fastapi import APIRouter, HTTPException, status, Depends 
from typing import List
from models.products import ProductoCrear, ProductoRespuesta, ProductoActualizar

router = APIRouter(prefix="/products", tags=["Products"])


products_db = {
    1: {"id": 1, "nombre": "Camisa", "precio": 29.99, "stock": 10, "categoria": "ropa"},
    2: {"id": 2, "nombre": "Zapatos", "precio": 59.99, "stock": 5, "categoria": "calzado"},
    3: {"id": 3, "nombre": "Gorra", "precio": 15.99, "stock": 20, "categoria": "ropa"},
}

def get_product_or_404(id: int):
    if products_db.get(id, None) is None:
        raise HTTPException(
            status_code= 404,
            detail= "Producto no encontrado"
        )
    return products_db[id]


# Crear nuevo producto
@router.post("", response_model= ProductoRespuesta, status_code = status.HTTP_201_CREATED)
def create_product(producto: ProductoCrear):
    new_id = max(products_db.keys()) + 1
    user_data = producto.model_dump()
    user_data["id"] = new_id
    products_db[new_id] = user_data
    return user_data


# Consulatr todos los productos
@router.get("", response_model= List[ProductoRespuesta])
def get_products():
    return list(products_db.values())

# Consultar productos por id
@router.get("/{id}")
def get_proudct_by_id(product: dict = Depends(get_product_or_404)):
    return product

# ELiminar producto
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, _: dict = Depends(get_product_or_404)):
    products_db.pop(id)

# Actualizar todo el producto
@router.put("/{id}", response_model= ProductoRespuesta)
def update_product(id: int, producto: ProductoCrear, _ = Depends(get_product_or_404)):
    producto_actualizado = {
        "id": id,
        **producto.model_dump()
    }
    products_db[id] = producto_actualizado
    return producto_actualizado

# Actualizar cualquier dato
@router.patch("/{id}", response_model= ProductoRespuesta)
def update_data(id: int, producto: ProductoActualizar, _= Depends(get_product_or_404)):

    cambios = producto.model_dump(exclude_none=True)

    products_db[id].update(cambios)
    return products_db[id]
