from datetime import date

from pydantic import BaseModel, Field

class IndexPerformanceParams(BaseModel):
    start_date: date = Field(..., description="YYYY-MM-DD")
    end_date: date = Field(..., description="YYYY-MM-DD")

class IndexCompositionParams(BaseModel):
    trade_date: date = Field(..., description="YYYY-MM-DD")

class CompositionChangesParams(BaseModel):
    start_date: date = Field(..., description="YYYY-MM-DD")
    end_date: date = Field(..., description="YYYY-MM-DD")

