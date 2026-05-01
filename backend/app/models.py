import enum


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"


class BusinessType(str, enum.Enum):
    sole_proprietorship = "sole_proprietorship"
    partnership = "partnership"
    pvt_ltd = "pvt_ltd"
    llp = "llp"
    public_ltd = "public_ltd"
