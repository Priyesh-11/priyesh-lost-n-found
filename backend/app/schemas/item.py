from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.item import ItemType, ItemStatus
from app.schemas.user import UserBasic

class CategoryOut(BaseModel):
    id: int
    name: str
    icon: Optional[str] = None

    class Config:
        from_attributes = True

class ItemImageBase(BaseModel):
    image_url: str
    thumbnail_url: Optional[str] = None
    is_primary: bool = False
    upload_order: int = 0

class ItemImageCreate(ItemImageBase):
    pass

class ItemImageOut(ItemImageBase):
    id: int

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    title: str
    description: str
    type: ItemType
    status: ItemStatus = ItemStatus.ACTIVE
    location: str
    date_lost: Optional[datetime] = None
    contact_method: Optional[str] = None
    category_id: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ItemType] = None
    status: Optional[ItemStatus] = None
    location: Optional[str] = None
    date_lost: Optional[datetime] = None
    contact_method: Optional[str] = None
    category_id: Optional[int] = None

class ItemOut(ItemBase):
    id: int
    user_id: int
    views_count: int
    is_approved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    images: List[ItemImageOut] = []
    owner: UserBasic
    category: CategoryOut
    claims_count: int = 0

    class Config:
        from_attributes = True

class ItemFilter(BaseModel):
    query: Optional[str] = None
    type: Optional[ItemType] = None
    status: Optional[ItemStatus] = None
    category_id: Optional[int] = None
    location: Optional[str] = None
    date_from: Optional[datetime] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    user_id: Optional[int] = None
