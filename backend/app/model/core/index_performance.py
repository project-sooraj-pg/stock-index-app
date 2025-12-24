from datetime import date

from app.model.serializable import SerializableBaseModel

class IndexPerformance(SerializableBaseModel):
    trade_date: date
    index_value: float
    daily_return_in_percentage: float
    cumulative_return_in_percentage: float
