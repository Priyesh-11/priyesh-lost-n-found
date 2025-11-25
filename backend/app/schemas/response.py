from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str = ""
    data: Optional[T] = None

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]
