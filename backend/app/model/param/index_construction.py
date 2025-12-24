from datetime import date
from typing import Optional

from pydantic import Field

from backend.app.model.serializable import SerializableBaseModel


class BuildIndexParams(SerializableBaseModel):
    start_date: date = Field(..., description="YYYY-MM-DD")
    end_date: Optional[date] = Field(None, description="YYYY-MM-DD (optional)")
