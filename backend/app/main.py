# ============================================================
# main.py — FastAPI Application Entry Point
# ============================================================
# This file bootstraps the FastAPI app, registers all route
# blueprints, applies middleware, and defines startup logic.
# ============================================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.middleware.cors import add_cors_middleware
from app.routes import auth_routes, merchant_routes, admin_routes, application_routes, upload_routes
from app.database import engine, Base

# ----- Create all database tables on startup -----
Base.metadata.create_all(bind=engine)

# ----- Initialize FastAPI app -----
app = FastAPI(
    title="Fintech Onboarding API",
    description="Merchant onboarding platform for payment services",
    version="1.0.0"
)

# ----- Apply CORS Middleware (allow React frontend to call this API) -----
add_cors_middleware(app)

# ----- Serve uploaded files as static assets -----
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ----- Register Route Blueprints -----
app.include_router(auth_routes.router,        prefix="/api/auth",         tags=["Auth"])
app.include_router(merchant_routes.router,    prefix="/api/merchant",     tags=["Merchant"])
app.include_router(admin_routes.router,       prefix="/api/admin",        tags=["Admin"])
app.include_router(application_routes.router, prefix="/api/application",  tags=["Application"])
app.include_router(upload_routes.router,      prefix="/api/upload",       tags=["Upload"])

# ----- Root Health Check -----
@app.get("/")
def root():
    return {"message": "Fintech Onboarding API is running!"}
