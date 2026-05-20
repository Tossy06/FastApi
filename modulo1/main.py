from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def root():
    return {"api": "Mi primera api", "version": "1.0"}

@app.get("/yo")
def user_data():
    return {"nombre": "David", "edad": 20, "lenguaje": "Python"}

@app.get("/yo/{dato}")
def user_w_data(dato: str):
    info = {
        "nombre": "David",
        "edad": 20,
        "lenguaje": "Python"
    }
    return {"dato": dato, "valor":info.get(dato, "")}


@app.get("/productos")
def query_products(limite: int = 10 , pagina: int= 1, buscar: Optional[str]= None):
    return {"limite": limite, "pagina": pagina, "buscar": buscar}

@app.get("/calcular")
def calculator(a: float, b:float, operacion: Optional[str]="suma"):
    operaciones = {
        "suma": lambda x, y: x + y,
        "resta": lambda x, y: x - y,
        "multi": lambda x, y: x * y
    }

    resultado = operaciones.get(operacion, operaciones["suma"])(a, b)

    return{
        "operacion": operacion if operacion in operaciones else "suma",
        "resultado": resultado
    }

@app.get("/usuarios/{id}/posts")
def user_post(id: int, limite: int = 5):
    posts =[
        {"id": i, "titulo": f"Post {i} del usuario {id}"}
        for i in range(1, limite + 1)
    ]
    return{
        "usuario_id": id,
        "limite": limite,
        "posts": posts
    }

@app.get("/usuarios/{id}")
def user_id(id: int):
    usuarios = {
        1: {"nombre": "Ana", "email": "ana@email.com", "activo": True},
        2: {"nombre": "Luis", "email": "luis@email.com", "activo": False},
        3: {"nombre": "María", "email": "maria@email.com", "activo": True},
    }

    return usuarios.get(id, {"error": "usuario no encontrado"})


    