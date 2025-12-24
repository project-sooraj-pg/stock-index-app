from datetime import date
from typing import List

from backend.app.model.serializable import SerializableBaseModel

class CompanyTicker(SerializableBaseModel):
    company_name: str
    ticker_symbol: str

class CompositionChangeDto(SerializableBaseModel):
    change_date: date
    added: List[CompanyTicker]
    removed: List[CompanyTicker]
