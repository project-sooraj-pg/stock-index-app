from datetime import date

from app.model.serializable import SerializableBaseModel

class CompositionChange(SerializableBaseModel):
    change_date: date
    company_name: str
    ticker_symbol: str
    action: str
