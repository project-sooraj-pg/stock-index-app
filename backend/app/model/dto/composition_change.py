from datetime import date
from typing import List

from pydantic import BaseModel


class CompanyTicker(BaseModel):
    company_name: str
    ticker_symbol: str

class CompositionChange(BaseModel):
    change_date: date
    added: List[CompanyTicker]
    removed: List[CompanyTicker]
