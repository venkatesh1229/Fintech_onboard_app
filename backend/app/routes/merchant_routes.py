from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserResponse)
def get_merchant_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/application", response_model=schemas.ApplicationResponse)
def get_merchant_application(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(models.MerchantApplication).filter(
        models.MerchantApplication.merchant_id == current_user.id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="No application found.")
    return application