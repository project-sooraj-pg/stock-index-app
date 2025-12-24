from typing import Optional

from backend.app.model.serializable import SerializableBaseModel

class ErrorDetail(SerializableBaseModel):
    message: str
    code: Optional[str] = None

class ErrorResponse(SerializableBaseModel):
    status: str = "ERROR"
    error: ErrorDetail