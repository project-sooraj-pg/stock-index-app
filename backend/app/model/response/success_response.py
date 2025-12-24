from typing import TypeVar, List, Generic

from pydantic.generics import GenericModel

T = TypeVar("T")

class SuccessResponse(GenericModel, Generic[T]):
    status: str = "SUCCESS"
    results: List[T]
