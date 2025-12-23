from datetime import date

from pydantic import BaseModel
from typing import List

class CompanyTicker(BaseModel):
    company_name: str
    ticker_symbol: str

class CompositionChange(BaseModel):
    change_date: date
    added: List[CompanyTicker]
    removed: List[CompanyTicker]
