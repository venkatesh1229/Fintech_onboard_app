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
from typing import Optional, List
from app import schemas
from app.dependencies import get_current_admin
from app.storage import list_applications, get_application_by_id, update_application

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
    _:      dict           = Depends(get_current_admin)
):
    """
    Admin views all merchant applications.
    Supports optional filtering by status and search by business name/email.
    """
    return list_applications(status=status, search=search, skip=skip, limit=limit)


# ============================================================
# GET SINGLE APPLICATION DETAIL
# GET /api/admin/applications/{id}
# ============================================================
@router.get("/applications/{app_id}", response_model=schemas.ApplicationResponse)
def get_application_detail(
    app_id: int,
    _:      dict = Depends(get_current_admin)
):
    """
    Admin views full details of one specific application,
    including uploaded documents.
    """
    application = get_application_by_id(app_id)
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
    _:           dict = Depends(get_current_admin)
):
    """
    Admin updates the status of an application (e.g., pending → approved)
    and optionally adds remarks/comments.
    """
    try:
        return update_application(app_id, update_data.status, update_data.remarks)
    except ValueError:
        raise HTTPException(status_code=404, detail="Application not found")
