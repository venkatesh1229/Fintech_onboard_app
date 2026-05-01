# storage.py — Local JSON-backed data storage for development
# This replaces the SQLAlchemy database layer with simple JSON files.

import json
import os
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.models import ApplicationStatus
from app.utils.hashing import hash_password

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "db.json")
DB_LOCK = threading.Lock()

DEFAULT_DB: Dict[str, Any] = {
    "users": [],
    "applications": [],
    "documents": [],
    "admins": [],
    "next_ids": {"users": 1, "applications": 1, "documents": 1, "admins": 1},
}


def _ensure_db_file() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DB, f, indent=2)


def _load_raw_db() -> Dict[str, Any]:
    _ensure_db_file()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_raw_db(db: Dict[str, Any]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _save_db(db: Dict[str, Any]) -> None:
    with DB_LOCK:
        _save_raw_db(db)


def _load_db() -> Dict[str, Any]:
    with DB_LOCK:
        return _load_raw_db()


def _increment_id(db: Dict[str, Any], key: str) -> int:
    next_id = db["next_ids"][key]
    db["next_ids"][key] = next_id + 1
    return next_id


def ensure_db() -> None:
    """Create the JSON file and seed a default admin if none exists."""
    db = _load_db()
    if len(db["admins"]) == 0:
        db["admins"].append({
            "id": _increment_id(db, "admins"),
            "username": "admin",
            "email": "admin@example.com",
            "hashed_password": hash_password("admin123"),
            "is_superadmin": True,
            "created_at": _now_iso(),
        })
        _save_db(db)


def _match_case_insensitive(value: str, candidate: str) -> bool:
    return value.strip().lower() == candidate.strip().lower()


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((u for u in db["users"] if _match_case_insensitive(u["email"], email)), None)


def get_user_by_mobile(mobile: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((u for u in db["users"] if u["mobile"] == mobile), None)


def get_user_by_pan(pan: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((u for u in db["users"] if _match_case_insensitive(u["pan_number"], pan)), None)


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((u for u in db["users"] if u["id"] == user_id), None)


def get_admin_by_email(email: str) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((a for a in db["admins"] if _match_case_insensitive(a["email"], email)), None)


def get_application_by_merchant_id(merchant_id: int) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((a for a in db["applications"] if a["merchant_id"] == merchant_id), None)


def get_application_by_id(app_id: int) -> Optional[Dict[str, Any]]:
    db = _load_db()
    return next((a for a in db["applications"] if a["id"] == app_id), None)


def get_documents_for_application(application_id: int) -> List[Dict[str, Any]]:
    db = _load_db()
    return [d for d in db["documents"] if d["application_id"] == application_id]


def _attach_details(application: Dict[str, Any]) -> Dict[str, Any]:
    application_copy = application.copy()
    merchant = get_user_by_id(application_copy["merchant_id"])
    application_copy["merchant"] = merchant or {}
    application_copy["documents"] = get_documents_for_application(application_copy["id"])
    return application_copy


def list_applications(
    status: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    db = _load_db()
    query = db["applications"]

    if status:
        query = [a for a in query if a["status"] == status]

    if search:
        search_lower = search.strip().lower()
        matched = []
        for application in query:
            merchant = get_user_by_id(application["merchant_id"])
            if merchant is None:
                continue
            if search_lower in merchant["business_name"].lower() or search_lower in merchant["email"].lower():
                matched.append(application)
        query = matched

    sliced = query[skip: skip + limit]
    return [_attach_details(application) for application in sliced]


def create_user(user_data: dict) -> Dict[str, Any]:
    db = _load_db()
    user_id = _increment_id(db, "users")
    user = {
        "id": user_id,
        "business_name": user_data["business_name"],
        "contact_person": user_data["contact_person"],
        "mobile": user_data["mobile"],
        "email": user_data["email"].strip().lower(),
        "business_type": user_data["business_type"],
        "pan_number": user_data["pan_number"].strip().upper(),
        "gst_number": user_data["gst_number"],
        "services": ",".join(user_data["services"]),
        "hashed_password": user_data["hashed_password"],
        "is_active": True,
        "created_at": _now_iso(),
    }
    db["users"].append(user)
    _save_db(db)
    return user


def create_application(merchant_id: int) -> Dict[str, Any]:
    db = _load_db()
    app_id = _increment_id(db, "applications")
    application = {
        "id": app_id,
        "merchant_id": merchant_id,
        "status": ApplicationStatus.pending.value,
        "remarks": None,
        "submitted_at": _now_iso(),
        "updated_at": None,
    }
    db["applications"].append(application)
    _save_db(db)
    return _attach_details(application)


def update_application(app_id: int, status: str, remarks: Optional[str]) -> Dict[str, Any]:
    db = _load_db()
    application = next((a for a in db["applications"] if a["id"] == app_id), None)
    if application is None:
        raise ValueError("Application not found")
    application["status"] = status
    application["remarks"] = remarks
    application["updated_at"] = _now_iso()
    _save_db(db)
    return _attach_details(application)


def create_document(application_id: int, doc_type: str, file_name: str, file_path: str) -> Dict[str, Any]:
    db = _load_db()
    document_id = _increment_id(db, "documents")
    document = {
        "id": document_id,
        "application_id": application_id,
        "doc_type": doc_type,
        "file_name": file_name,
        "file_path": file_path,
        "uploaded_at": _now_iso(),
    }
    db["documents"].append(document)
    _save_db(db)
    return document
