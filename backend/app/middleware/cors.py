# ============================================================
# middleware/cors.py — Cross-Origin Resource Sharing
# ============================================================
# Browsers block requests from one domain to another by
# default (CORS policy). This middleware tells the browser
# that our React frontend (localhost:3000) is allowed to
# call this FastAPI backend (localhost:8000).
# ============================================================

from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    print("CORS middleware configured: allow_origins=['*'], allow_credentials=False")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )