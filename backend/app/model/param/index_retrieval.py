from datetime import date

from pydantic import Field

from backend.app.model.serializable import SerializableBaseModel


class IndexPerformanceParams(SerializableBaseModel):
    start_date: date = Field(..., description="YYYY-MM-DD")
    end_date: date = Field(..., description="YYYY-MM-DD")

class IndexCompositionParams(SerializableBaseModel):
    trade_date: date = Field(..., description="YYYY-MM-DD")

class CompositionChangesParams(SerializableBaseModel):
    start_date: date = Field(..., description="YYYY-MM-DD")
    end_date: date = Field(..., description="YYYY-MM-DD")

