from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

class BuildIndexParams(BaseModel):
    start_date: date = Field(..., description="YYYY-MM-DD")
    end_date: Optional[date] = Field(None, description="YYYY-MM-DD (optional)")
