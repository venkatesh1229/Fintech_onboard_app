# ============================================================
# routes/upload_routes.py — Document Upload API
# ============================================================
# POST /api/upload/document
#   → Merchant uploads a file (PAN card, GST cert, etc.)
#   → File is saved to /uploads/ folder on the server
#   → A Document record is stored in local JSON storage
# ============================================================

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.dependencies import get_current_user
from app.storage import get_application_by_merchant_id, create_document

router = APIRouter()

# Folder where files will be saved (must exist)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed document types
ALLOWED_DOC_TYPES = ["pan_card", "gst_certificate", "bank_statement", "company_registration"]

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


@router.post("/document")
async def upload_document(
    doc_type: str        = Form(..., description="One of: pan_card, gst_certificate, bank_statement, company_registration"),
    file:     UploadFile = File(...),
    current_user: dict   = Depends(get_current_user)
):
    """
    Upload a document for the merchant's application.
    """
    if doc_type not in ALLOWED_DOC_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type. Allowed: {ALLOWED_DOC_TYPES}")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, JPG, JPEG, PNG files are allowed")

    application = get_application_by_merchant_id(current_user["id"])
    if not application:
        raise HTTPException(status_code=404, detail="Submit your application first before uploading documents")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    document = create_document(application["id"], doc_type, file.filename, file_path)

    return {
        "message": "Document uploaded successfully",
        "doc_id": document["id"],
        "file_name": document["file_name"],
        "doc_type": document["doc_type"],
    }
