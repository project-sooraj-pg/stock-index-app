from datetime import date

from pydantic import BaseModel

class ExportIndexComposition(BaseModel):
    trade_date: date
    company_name: str
    ticker_symbol: str
    market_cap_rank: int

