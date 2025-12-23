from typing import Optional

from pydantic import BaseModel

class ErrorDetail(BaseModel):
    message: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str = "ERROR"
    error: ErrorDetail