from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate, ItemFilter, CategoryOut
from app.crud.crud_item import item as crud_item
from app.models.item import Category
from app.models.user import User
from app.services.image_service import image_service
from app.models.item_image import ItemImage
from app.schemas.claim import Claim, ClaimCreate
from app.crud.crud_claim import claim as crud_claim
from app.models.item import ItemType

router = APIRouter()

@router.get("/categories", response_model=List[CategoryOut])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve item categories.
    """
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@router.get("/", response_model=List[ItemOut])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = "active",  # Default to active items only
    type: str = None,
    category_id: int = None,
    query: str = None,
    user_id: int = None,
) -> Any:
    # Support for viewing all items by passing status=all
    if status and status.lower() == "all":
        status = None
        
    filters = ItemFilter(
        status=status,
        type=type,
        category_id=category_id,
        query=query,
        user_id=user_id
    )
    items = crud_item.get_multi_with_filters(
        db, filters=filters, skip=skip, limit=limit
    )
    
    # Add claims count to each item
    # Optimize claims count using a single query
    item_ids = [item.id for item in items]
    claims_counts = db.query(
        crud_claim.model.item_id, func.count(crud_claim.model.id).label('count')
    ).filter(
        crud_claim.model.item_id.in_(item_ids),
        crud_claim.model.status == 'pending'
    ).group_by(crud_claim.model.item_id).all()
    
    claims_map = {item_id: count for item_id, count in claims_counts}
    
    for item in items:
        item.claims_count = claims_map.get(item.id, 0)
    
    return items

@router.post("/", response_model=ItemOut)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    item = crud_item.create_with_owner(db=db, obj_in=item_in, user_id=current_user.id)
    return item

@router.get("/{id}", response_model=ItemOut)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Increment views
    crud_item.increment_views(db=db, item_id=id)
    
    # Add claims count
    claims_count = db.query(crud_claim.model).filter(
        crud_claim.model.item_id == id,
        crud_claim.model.status == 'pending'
    ).count()
    item.claims_count = claims_count
    
    return item

@router.post("/{id}/images")
async def upload_item_images(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    uploaded_urls = []
    for file in files:
        if image_service.validate_image(file):
            url = await image_service.upload_image(file)
            if url:
                db_image = ItemImage(
                    item_id=id,
                    image_url=url,
                    is_primary=len(item.images) == 0 # First image is primary
                )
                db.add(db_image)
                uploaded_urls.append(url)
    
    db.commit()
    return {"uploaded": uploaded_urls}

@router.post("/{id}/claim", response_model=Claim)
def create_claim(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    claim_in: ClaimCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit a claim for a found item.
    """
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if item is 'found' type
    if item.type != ItemType.FOUND:
        raise HTTPException(status_code=400, detail="Only found items can be claimed")
    
    # Check if user is the owner (can't claim own item)
    if item.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot claim your own reported item")
    
    # Check if already claimed by this user
    existing_claims = crud_claim.get_by_item(db=db, item_id=id)
    for claim in existing_claims:
        if claim.claimant_id == current_user.id:
            raise HTTPException(status_code=400, detail="You have already claimed this item")

    claim = crud_claim.create_with_owner(
        db=db, obj_in=claim_in, item_id=id, claimant_id=current_user.id
    )
    return claim

@router.post("/{id}/claim-proof-upload")
async def upload_claim_proof(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload proof images for a claim. Anyone can upload proof for claims.
    """
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.type != ItemType.FOUND:
        raise HTTPException(status_code=400, detail="Only found items can have claim proofs")
    
    uploaded_urls = []
    for file in files:
        if image_service.validate_image(file):
            url = await image_service.upload_image(file)
            if url:
                uploaded_urls.append(url)
    
    return {"uploaded": uploaded_urls}
from app.services.matching_service import matching_service

@router.get("/{item_id}/matches", response_model=List[dict])
def get_item_matches(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get potential matches for a specific item.
    """
    item = crud_item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    # Only owner or admin can see matches
    if not crud_user.is_superuser(current_user) and (item.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
        
    matches = matching_service.find_potential_matches(db, item)
    return matches
