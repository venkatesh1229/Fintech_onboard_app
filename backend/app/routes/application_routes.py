# ============================================================
# routes/application_routes.py — Merchant Application APIs
# ============================================================
# POST /api/application/submit    → Merchant submits application
# GET  /api/application/status    → Merchant checks their own status
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.dependencies import get_current_user
from app.storage import get_application_by_merchant_id, create_application

router = APIRouter()


# ============================================================
# SUBMIT APPLICATION
# POST /api/application/submit
# ============================================================
@router.post("/submit", response_model=schemas.ApplicationResponse)
def submit_application(current_user: dict = Depends(get_current_user)):
    """
    A merchant submits their onboarding application.
    Each merchant can only have one application.
    """
    existing = get_application_by_merchant_id(current_user["id"])

    if existing:
        raise HTTPException(status_code=400, detail="Application already submitted")

    return create_application(current_user["id"])


# ============================================================
# GET APPLICATION STATUS
# GET /api/application/status
# ============================================================
@router.get("/status", response_model=schemas.ApplicationResponse)
def get_application_status(current_user: dict = Depends(get_current_user)):
    """
    Merchant can check the current status of their application.
    Also returns any admin remarks.
    """
    application = get_application_by_merchant_id(current_user["id"])

    if not application:
        raise HTTPException(status_code=404, detail="No application found. Please submit first.")

    return application
