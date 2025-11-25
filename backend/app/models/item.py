from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ItemType(str, enum.Enum):
    LOST = "lost"
    FOUND = "found"

class ItemStatus(str, enum.Enum):
    ACTIVE = "active"
    CLAIMED = "claimed"
    RESOLVED = "resolved"
    ARCHIVED = "archived"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    icon = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    type = Column(Enum(ItemType), nullable=False, index=True)
    status = Column(Enum(ItemStatus), default=ItemStatus.ACTIVE, index=True)
    location = Column(String(255), nullable=False, index=True)
    date_lost = Column(DateTime(timezone=True), index=True)
    contact_method = Column(String(255)) # e.g., "email", "phone", "chat"
    is_approved = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="items")
    category = relationship("Category", back_populates="items")
    images = relationship("ItemImage", back_populates="item", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="item")
    claims = relationship("Claim", back_populates="item", cascade="all, delete-orphan")
