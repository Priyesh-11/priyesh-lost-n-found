from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ClaimStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    claimant_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.PENDING, index=True)
    proof_description = Column(Text, nullable=False)
    proof_image_url = Column(String(255))
    admin_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    item = relationship("Item", back_populates="claims")
    claimant = relationship("User", back_populates="claims")
