from datetime import date

from pydantic import BaseModel

class IndexPerformance(BaseModel):
    trade_date: date
    index_value: float
    daily_return_in_percentage: float
    cumulative_return_in_percentage: float
