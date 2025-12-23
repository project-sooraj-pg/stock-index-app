from datetime import date

from pydantic import BaseModel

class IndexComposition(BaseModel):
    company_name: str
    ticker_symbol: str
    market_cap_rank: int
