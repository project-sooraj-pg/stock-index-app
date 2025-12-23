from datetime import date

from pydantic import BaseModel

class ExportCompositionChange(BaseModel):
    change_date: date
    company_name: str
    ticker_symbol: str
    action: str
