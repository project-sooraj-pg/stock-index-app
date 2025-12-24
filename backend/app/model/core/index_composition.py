from datetime import date

from app.model.serializable import SerializableBaseModel

class IndexComposition(SerializableBaseModel):
    trade_date: date
    company_name: str
    ticker_symbol: str
    market_cap_rank: int
