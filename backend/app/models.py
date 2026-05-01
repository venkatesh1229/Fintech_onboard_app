# ============================================================
# models.py — SQLAlchemy ORM Models (Database Tables)
# ============================================================
# Each class here maps to a MySQL table. SQLAlchemy will
# auto-create these tables when Base.metadata.create_all()
# is called in main.py.
# ============================================================

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

# ---- Enums: Allowed values for certain columns ----

class ApplicationStatus(str, enum.Enum):
    pending      = "pending"
    under_review = "under_review"
    approved     = "approved"
    rejected     = "rejected"

class BusinessType(str, enum.Enum):
    sole_proprietorship = "sole_proprietorship"
    partnership         = "partnership"
    pvt_ltd             = "pvt_ltd"
    llp                 = "llp"
    public_ltd          = "public_ltd"

# ============================================================
# TABLE: users — Merchant accounts
# ============================================================
class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    business_name   = Column(String(200), nullable=False)
    contact_person  = Column(String(100), nullable=False)
    mobile          = Column(String(15),  nullable=False, unique=True)
    email           = Column(String(100), nullable=False, unique=True, index=True)
    business_type   = Column(Enum(BusinessType), nullable=False)
    pan_number      = Column(String(10),  nullable=False, unique=True)
    gst_number      = Column(String(15),  nullable=False)
    services        = Column(String(300), nullable=False)  # Comma-separated: "PayIn,Payout,UPI"
    hashed_password = Column(String(200), nullable=False)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    # One merchant -> one application
    application     = relationship("MerchantApplication", back_populates="merchant", uselist=False)


# ============================================================
# TABLE: merchant_applications — Onboarding applications
# ============================================================
class MerchantApplication(Base):
    __tablename__ = "merchant_applications"

    id          = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status      = Column(Enum(ApplicationStatus), default=ApplicationStatus.pending)
    remarks     = Column(Text, nullable=True)        # Admin adds notes here
    submitted_at= Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    merchant    = relationship("User", back_populates="application")
    documents   = relationship("Document", back_populates="application")


# ============================================================
# TABLE: documents — Uploaded files per application
# ============================================================
class Document(Base):
    __tablename__ = "documents"

    id             = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("merchant_applications.id"), nullable=False)
    doc_type       = Column(String(50), nullable=False)    # e.g., "pan_card", "gst_certificate"
    file_name      = Column(String(200), nullable=False)   # Original file name
    file_path      = Column(String(500), nullable=False)   # Server path to the file
    uploaded_at    = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to application
    application    = relationship("MerchantApplication", back_populates="documents")


# ============================================================
# TABLE: admin_users — Separate admin accounts
# ============================================================
class AdminUser(Base):
    __tablename__ = "admin_users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50), nullable=False, unique=True)
    email           = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    is_superadmin   = Column(Boolean, default=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
