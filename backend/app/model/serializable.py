from datetime import date, datetime

from pydantic import BaseModel


class SerializableBaseModel(BaseModel):
        class Config:
            json_encoders = {
                date: lambda v: v.isoformat(),
                datetime: lambda v: v.isoformat(),
            }