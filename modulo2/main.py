from fastapi import FastAPI, HTTPException, status
from typing import List
from models.products import ProductoCrear, ProductoRespuesta, ProductoActualizar
app = FastAPI()

productos_db = {
    1: {"id": 1, "nombre": "Camisa", "precio": 29.99, "stock": 10, "categoria": "ropa"},
    2: {"id": 2, "nombre": "Zapatos", "precio": 59.99, "stock": 5, "categoria": "calzado"},
    3: {"id": 3, "nombre": "Gorra", "precio": 15.99, "stock": 20, "categoria": "ropa"},
}

# Crear nuevo producto
@app.post("/productos", response_model= ProductoRespuesta, status_code = status.HTTP_201_CREATED)
def create_product(producto: ProductoCrear):
    new_id = max(productos_db.keys()) + 1
    user_data = producto.model_dump()
    user_data["id"] = new_id
    productos_db[new_id] = user_data
    return user_data


# Consulatr todos los productos
@app.get("/productos", response_model= List[ProductoRespuesta])
def get_products():
    return list(productos_db.values())

# Consultar productos por id
@app.get("/productos/{id}")
def get_prudct_by_id(id: int):
    try:
        return productos_db[id]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

# ELiminar producto
@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    if productos_db.pop(id, None) is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

# Actualizar todo el producto
@app.put("/productos/{id}", response_model= ProductoRespuesta)
def update_product(id: int, producto: ProductoCrear):
    if productos_db.get(id) is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )
    producto_actualizado = {
        "id": id,
        **producto.model_dump()
    }
    productos_db[id] = producto_actualizado
    return producto_actualizado

# Actualizar cualquier dato
@app.patch("/productos/{id}", response_model= ProductoRespuesta)
def update_data(id: int, producto: ProductoActualizar):
    if productos_db.get(id) is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )
    cambios = producto.model_dump(exclude_none=True)

    productos_db[id].update(cambios)
    return productos_db[id]
