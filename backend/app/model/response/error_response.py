from app.model.serializable import SerializableBaseModel

class ErrorResponse(SerializableBaseModel):
    status: str = "ERROR"
    error: str