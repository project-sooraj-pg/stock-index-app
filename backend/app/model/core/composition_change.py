from datetime import date

from pydantic import BaseModel

class CompositionChange(BaseModel):
    change_date: date
    company_name: str
    ticker_symbol: str
    action: str
