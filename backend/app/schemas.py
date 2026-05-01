# ============================================================
# schemas.py — Pydantic Schemas (Request & Response Models)
# ============================================================
# Pydantic validates incoming request data and shapes API
# responses. Think of these as "contracts" between frontend
# and backend — the frontend MUST send these exact fields.
# ============================================================

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from app.models import ApplicationStatus, BusinessType


# ============================================================
# AUTH SCHEMAS
# ============================================================

class LoginRequest(BaseModel):
    """Schema for merchant/admin login"""
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    """Returned after successful login"""
    access_token: str
    token_type:   str = "bearer"
    role:         str  # "merchant" or "admin"


# ============================================================
# USER / MERCHANT SCHEMAS
# ============================================================

class UserCreate(BaseModel):
    """Schema for merchant registration — all fields required"""
    business_name:  str
    contact_person: str
    mobile:         str
    email:          EmailStr
    password:       str
    business_type:  BusinessType
    pan_number:     str
    gst_number:     str
    services:       List[str]  # ["PayIn", "Payout", "UPI"]

    @validator("pan_number")
    def pan_must_be_valid(cls, v):
        """PAN must be exactly 10 alphanumeric characters"""
        if len(v) != 10:
            raise ValueError("PAN number must be 10 characters")
        return v.upper()

    @validator("mobile")
    def mobile_must_be_valid(cls, v):
        """Basic mobile number check"""
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Mobile must be 10 digits")
        return v


class UserResponse(BaseModel):
    """Returned when merchant data is read — never includes password"""
    id:             int
    business_name:  str
    contact_person: str
    email:          str
    mobile:         str
    business_type:  str
    pan_number:     str
    gst_number:     str
    services:       str
    created_at:     str

    class Config:
        from_attributes = True


# ============================================================
# APPLICATION SCHEMAS
# ============================================================

class ApplicationCreate(BaseModel):
    """Merchant submits onboarding application"""
    # Currently no extra fields — merchant_id comes from JWT token
    pass


class StatusUpdateRequest(BaseModel):
    """Admin updates the application status and optional remarks"""
    status:  ApplicationStatus
    remarks: Optional[str] = None


class DocumentOut(BaseModel):
    """Document details returned in application response"""
    id:          int
    doc_type:    str
    file_name:   str
    file_path:   str
    uploaded_at: str

    class Config:
        from_attributes = True


class ApplicationResponse(BaseModel):
    """Full application details including merchant info and documents"""
    id:           int
    status:       str
    remarks:      Optional[str]
    submitted_at: str
    merchant:     UserResponse
    documents:    List[DocumentOut]

    class Config:
        from_attributes = True


# ============================================================
# ADMIN SCHEMAS
# ============================================================

class AdminCreate(BaseModel):
    """Admin user creation (done manually or via seed script)"""
    username: str
    email:    EmailStr
    password: str
