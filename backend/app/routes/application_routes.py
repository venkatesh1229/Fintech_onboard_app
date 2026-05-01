# ============================================================
# routes/application_routes.py — Merchant Application APIs
# ============================================================
# POST /api/application/submit    → Merchant submits application
# GET  /api/application/status    → Merchant checks their own status
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()


# ============================================================
# SUBMIT APPLICATION
# POST /api/application/submit
# ============================================================
@router.post("/submit", response_model=schemas.ApplicationResponse)
def submit_application(
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # Requires JWT
):
    """
    A merchant submits their onboarding application.
    Each merchant can only have one application.
    """
    # Check if application already submitted
    existing = db.query(models.MerchantApplication)\
                 .filter(models.MerchantApplication.merchant_id == current_user.id)\
                 .first()

    if existing:
        raise HTTPException(status_code=400, detail="Application already submitted")

    # Create new application with default status = "pending"
    application = models.MerchantApplication(merchant_id=current_user.id)
    db.add(application)
    db.commit()
    db.refresh(application)

    return application


# ============================================================
# GET APPLICATION STATUS
# GET /api/application/status
# ============================================================
@router.get("/status", response_model=schemas.ApplicationResponse)
def get_application_status(
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Merchant can check the current status of their application.
    Also returns any admin remarks.
    """
    application = db.query(models.MerchantApplication)\
                    .filter(models.MerchantApplication.merchant_id == current_user.id)\
                    .first()

    if not application:
        raise HTTPException(status_code=404, detail="No application found. Please submit first.")

    return application
