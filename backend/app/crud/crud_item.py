from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.crud.base import CRUDBase
from app.models.item import Item, ItemStatus, ItemType
from app.schemas.item import ItemCreate, ItemUpdate, ItemFilter

class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, user_id: int
    ) -> Item:
        obj_in_data = obj_in.model_dump()
        db_obj = Item(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_with_filters(
        self, db: Session, *, filters: ItemFilter, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        query = db.query(Item)
        
        if filters.status:
            query = query.filter(Item.status == filters.status)
        elif not filters.user_id:
            # Default to active items if no status specified for public list, unless filtering by user
            query = query.filter(Item.status == ItemStatus.ACTIVE)
            
        if filters.type:
            query = query.filter(Item.type == filters.type)
            
        if filters.category_id:
            query = query.filter(Item.category_id == filters.category_id)
            
        if filters.location:
            query = query.filter(Item.location.ilike(f"%{filters.location}%"))
            
        if filters.query:
            search = f"%{filters.query}%"
            query = query.filter(
                or_(
                    Item.title.ilike(search),
                    Item.description.ilike(search)
                )
            )
            
        if filters.date_from:
            query = query.filter(Item.date_lost >= filters.date_from)
            
        if filters.date_to:
            query = query.filter(Item.date_lost <= filters.date_to)

        if filters.user_id:
            query = query.filter(Item.user_id == filters.user_id)
            
        return query.order_by(desc(Item.created_at)).offset(skip).limit(limit).all()

    def increment_views(self, db: Session, *, item_id: int) -> Optional[Item]:
        item = db.query(Item).filter(Item.id == item_id).first()
        if item:
            item.views_count += 1
            db.add(item)
            db.commit()
            db.refresh(item)
        return item

item = CRUDItem(Item)
