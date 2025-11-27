from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.claim import Claim, ClaimCreate
from app.crud.crud_claim import claim as crud_claim
from app.crud.crud_item import item as crud_item
from app.models.user import User
from app.models.item import ItemType

router = APIRouter()



@router.get("/my-claims", response_model=List[Claim])
def read_my_claims(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve current user's claims with item details.
    """
    claims = crud_claim.get_by_user(db=db, user_id=current_user.id)
    
    # Enrich claims with item and claimant details
    enriched_claims = []
    for claim in claims:
        item = crud_item.get(db=db, id=claim.item_id)
        claim_dict = {
            "id": claim.id,
            "item_id": claim.item_id,
            "claimant_id": claim.claimant_id,
            "status": claim.status,
            "proof_description": claim.proof_description,
            "proof_image_url": claim.proof_image_url,
            "admin_notes": claim.admin_notes,
            "created_at": claim.created_at,
            "updated_at": claim.updated_at,
            "claimant_name": current_user.full_name or current_user.username,
            "claimant_email": current_user.email,
            "item_title": item.title if item else "Unknown Item",
            "item_type": item.type if item else None,
            "item_category": item.category.name if (item and item.category) else None,
        }
        enriched_claims.append(claim_dict)
    
    return enriched_claims

@router.get("/{id}", response_model=Claim)
def read_claim(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get claim by ID.
    """
    claim = crud_claim.get(db=db, id=id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    if claim.claimant_id != current_user.id and current_user.role_id != 3: # Admin ID is 3
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return claim
