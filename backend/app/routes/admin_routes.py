# ============================================================
# routes/admin_routes.py — Admin Panel APIs
# ============================================================
# All routes here require admin JWT token (role="admin").
#
# GET  /api/admin/applications           → List all applications
# GET  /api/admin/applications/{id}      → Single application detail
# PUT  /api/admin/applications/{id}/status → Update status + remarks
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_admin

router = APIRouter()


# ============================================================
# GET ALL APPLICATIONS (with search/filter)
# GET /api/admin/applications?status=pending&search=xyz
# ============================================================
@router.get("/applications", response_model=List[schemas.ApplicationResponse])
def get_all_applications(
    status: Optional[str]  = Query(None, description="Filter by status"),
    search: Optional[str]  = Query(None, description="Search by business name or email"),
    skip:   int            = Query(0,    description="Pagination offset"),
    limit:  int            = Query(20,   description="Results per page"),
    db:     Session        = Depends(get_db),
    _:      models.AdminUser = Depends(get_current_admin)  # Requires admin JWT
):
    """
    Admin views all merchant applications.
    Supports optional filtering by status and search by business name/email.
    """
    # Start with base query joining application + merchant
    query = db.query(models.MerchantApplication)\
              .join(models.User)

    # Apply status filter if provided
    if status:
        query = query.filter(models.MerchantApplication.status == status)

    # Apply search filter across business name and email
    if search:
        query = query.filter(
            models.User.business_name.contains(search) |
            models.User.email.contains(search)
        )

    # Paginate and return
    return query.offset(skip).limit(limit).all()


# ============================================================
# GET SINGLE APPLICATION DETAIL
# GET /api/admin/applications/{id}
# ============================================================
@router.get("/applications/{app_id}", response_model=schemas.ApplicationResponse)
def get_application_detail(
    app_id: int,
    db:     Session          = Depends(get_db),
    _:      models.AdminUser = Depends(get_current_admin)
):
    """
    Admin views full details of one specific application,
    including uploaded documents.
    """
    application = db.query(models.MerchantApplication)\
                    .filter(models.MerchantApplication.id == app_id)\
                    .first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


# ============================================================
# UPDATE APPLICATION STATUS
# PUT /api/admin/applications/{id}/status
# ============================================================
@router.put("/applications/{app_id}/status", response_model=schemas.ApplicationResponse)
def update_application_status(
    app_id:      int,
    update_data: schemas.StatusUpdateRequest,
    db:          Session          = Depends(get_db),
    _:           models.AdminUser = Depends(get_current_admin)
):
    """
    Admin updates the status of an application (e.g., pending → approved)
    and optionally adds remarks/comments.
    """
    application = db.query(models.MerchantApplication)\
                    .filter(models.MerchantApplication.id == app_id)\
                    .first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Apply the status update
    application.status  = update_data.status
    application.remarks = update_data.remarks

    db.commit()
    db.refresh(application)

    return application
