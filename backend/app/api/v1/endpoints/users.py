from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import UserOut, UserUpdate, UserBasic
from app.crud.crud_user import user as crud_user
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user

@router.put("/me", response_model=UserOut)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=UserBasic)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    user = crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
