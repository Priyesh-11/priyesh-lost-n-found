from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.role import Role
from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str
    permissions: Optional[dict] = None

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permissions: Optional[dict] = None

class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

role = CRUDRole(Role)
