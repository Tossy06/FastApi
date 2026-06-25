from fastapi import FastAPI
from core.config import setup_cors
from routers import items, auth

app = FastAPI()
setup_cors(app)

@app.get("/status")
def get_status():
    return {"status": "ok", "message": "Gallery API running"}

app.include_router(items.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")



    