from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # Get or create the "user" role dynamically
        from app.models.role import Role
        from sqlalchemy.exc import IntegrityError
        import logging
        
        logger = logging.getLogger(__name__)
        
        # Get or create user role
        user_role = db.query(Role).filter(Role.name == "user").first()
        if not user_role:
            # Role doesn't exist - create it automatically
            logger.warning("User role not found, creating it automatically")
            try:
                user_role = Role(name="user", permissions={"read": True, "write": True})
                db.add(user_role)
                db.flush()  # Flush to get the ID without committing
                db.refresh(user_role)
                logger.info(f"Created user role with id={user_role.id}")
            except IntegrityError:
                # Race condition: another request created it, fetch it
                db.rollback()
                user_role = db.query(Role).filter(Role.name == "user").first()
                if not user_role:
                    raise ValueError("Failed to get or create user role")
        
        # Ensure admin role also exists (for future use, non-blocking)
        try:
            admin_role = db.query(Role).filter(Role.name == "admin").first()
            if not admin_role:
                logger.warning("Admin role not found, creating it automatically")
                admin_role = Role(name="admin", permissions={"all": True})
                db.add(admin_role)
                db.flush()
        except IntegrityError:
            # Admin role was created by another request, ignore
            db.rollback()
        
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            username=obj_in.username,
            role_id=user_role.id,  # Use dynamically found or created role ID
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user = CRUDUser(User)
