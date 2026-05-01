# ============================================================
# routes/upload_routes.py — Document Upload API
# ============================================================
# POST /api/upload/document
#   → Merchant uploads a file (PAN card, GST cert, etc.)
#   → File is saved to /uploads/ folder on the server
#   → A Document record is created in the database
# ============================================================

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.dependencies import get_current_user

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
    db:       Session    = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Upload a document for the merchant's application.
    
    Steps:
    1. Validate doc_type and file extension
    2. Check the merchant has a submitted application
    3. Save file to disk with a unique name
    4. Store the file path in the documents table
    """
    # Step 1: Validate document type
    if doc_type not in ALLOWED_DOC_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type. Allowed: {ALLOWED_DOC_TYPES}")

    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, JPG, JPEG, PNG files are allowed")

    # Step 2: Find the merchant's application
    application = db.query(models.MerchantApplication)\
                    .filter(models.MerchantApplication.merchant_id == current_user.id)\
                    .first()

    if not application:
        raise HTTPException(status_code=404, detail="Submit your application first before uploading documents")

    # Step 3: Generate a unique filename to avoid collisions
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path   = os.path.join(UPLOAD_DIR, unique_name)

    # Write the file to disk
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Step 4: Save document record in the database
    document = models.Document(
        application_id = application.id,
        doc_type       = doc_type,
        file_name      = file.filename,  # Original name for display
        file_path      = file_path       # Server path for retrieval
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message":   "Document uploaded successfully",
        "doc_id":    document.id,
        "file_name": document.file_name,
        "doc_type":  document.doc_type
    }
