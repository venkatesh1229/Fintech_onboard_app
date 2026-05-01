from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.dependencies import get_current_user
from app.storage import get_application_by_merchant_id

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_merchant_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/application", response_model=schemas.ApplicationResponse)
def get_merchant_application(current_user: dict = Depends(get_current_user)):
    application = get_application_by_merchant_id(current_user["id"])
    if not application:
        raise HTTPException(status_code=404, detail="No application found.")
    return application