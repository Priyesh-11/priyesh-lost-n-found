from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.claim import Claim, ClaimStatus
from app.schemas.claim import ClaimCreate, ClaimUpdate

class CRUDClaim(CRUDBase[Claim, ClaimCreate, ClaimUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ClaimCreate, item_id: int, claimant_id: int
    ) -> Claim:
        db_obj = Claim(
            item_id=item_id,
            claimant_id=claimant_id,
            proof_description=obj_in.proof_description,
            proof_image_url=obj_in.proof_image_url,
            status=ClaimStatus.PENDING
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_item(self, db: Session, *, item_id: int) -> List[Claim]:
        return db.query(Claim).filter(Claim.item_id == item_id).all()

    def get_by_user(self, db: Session, *, user_id: int) -> List[Claim]:
        return db.query(Claim).filter(Claim.claimant_id == user_id).all()

    def get_multi_by_status(
        self, db: Session, *, status: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Claim]:
        if status:
            return db.query(Claim).filter(Claim.status == status).offset(skip).limit(limit).all()
        return db.query(Claim).offset(skip).limit(limit).all()

claim = CRUDClaim(Claim)
