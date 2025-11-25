from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.claim import Claim, ClaimUpdate
from app.schemas.item import ItemOut
from app.crud.crud_claim import claim as crud_claim
from app.crud.crud_item import item as crud_item
from app.models.user import User
from app.models.claim import ClaimStatus
from app.models.item import ItemStatus

router = APIRouter()

def check_admin_permissions(current_user: User):
    if current_user.role_id != 2: # Admin Role ID
        raise HTTPException(status_code=403, detail="Not enough permissions")

@router.get("/claims", response_model=List[Claim])
def read_all_claims(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all claims (Admin only).
    """
    check_admin_permissions(current_user)
    claims = crud_claim.get_multi_by_status(db, status=status, skip=skip, limit=limit)
    
    # Enhance claims with claimant and item details
    for claim in claims:
        if claim.claimant:
            claim.claimant_name = claim.claimant.full_name or claim.claimant.username
            claim.claimant_email = claim.claimant.email
        if claim.item:
            claim.item_title = claim.item.title
    
    return claims

from app.services.email_service import email_service

@router.put("/claims/{id}/verify", response_model=Claim)
def verify_claim(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    claim_update: ClaimUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Verify or Reject a claim (Admin only).
    """
    check_admin_permissions(current_user)
    claim = crud_claim.get(db=db, id=id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    claim = crud_claim.update(db=db, db_obj=claim, obj_in=claim_update)
    
    # If claim is verified, update item status to CLAIMED (pending resolution)
    if claim.status == ClaimStatus.VERIFIED:
        item = crud_item.get(db=db, id=claim.item_id)
        if item:
            item.status = ItemStatus.CLAIMED
            db.add(item)
            db.commit()
            
    # Send email notification
    if claim.claimant and claim.item:
        email_service.send_claim_status_email(
            email_to=claim.claimant.email,
            username=claim.claimant.full_name or claim.claimant.username,
            item_title=claim.item.title,
            status=claim.status,
            admin_notes=claim.admin_notes
        )
            
    return claim

@router.put("/items/{id}/resolve", response_model=ItemOut)
def resolve_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark item as returned/resolved and award reputation (Admin only).
    """
    check_admin_permissions(current_user)
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.status = ItemStatus.RESOLVED
    db.add(item)
    
    # Award reputation to the finder (owner of the item)
    finder = item.owner
    finder.reputation_score += 10
    db.add(finder)
    
    db.commit()
    db.refresh(item)
    return item
