from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    status: str = "SUCCESS"
    result: T