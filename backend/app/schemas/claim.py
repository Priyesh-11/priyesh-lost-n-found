from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.claim import ClaimStatus

# Shared properties
class ClaimBase(BaseModel):
    proof_description: str
    proof_image_url: Optional[str] = None

# Properties to receive via API on creation
class ClaimCreate(ClaimBase):
    pass

# Properties to receive via API on update
class ClaimUpdate(BaseModel):
    status: Optional[ClaimStatus] = None
    admin_notes: Optional[str] = None

# Properties shared by models stored in DB
class ClaimInDBBase(ClaimBase):
    id: int
    item_id: int
    claimant_id: int
    status: ClaimStatus
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Claim(ClaimInDBBase):
    claimant_name: Optional[str] = None
    claimant_email: Optional[str] = None
    item_title: Optional[str] = None
    item_type: Optional[str] = None
    item_category: Optional[str] = None

# Additional properties stored in DB
class ClaimInDB(ClaimInDBBase):
    pass
