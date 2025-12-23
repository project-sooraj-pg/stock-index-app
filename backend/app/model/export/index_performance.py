from datetime import date

from pydantic import BaseModel

class ExportIndexPerformance(BaseModel):
    trade_date: date
    index_value: float
    daily_return: float
    cumulative_return: float
