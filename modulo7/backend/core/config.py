from fastapi.middleware.cors import CORSMiddleware

CORS_ORIGINS = ["http://127.0.0.1:5500"]

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
