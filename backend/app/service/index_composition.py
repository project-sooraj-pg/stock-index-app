from datetime import date
from typing import List

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import ApplicationException
from app.model.core.index_composition import IndexComposition
from app.model.core.composition_change import CompositionChange


class IndexCompositionService:

    async def get_index_composition(self, session: AsyncSession, trade_date: date = None) -> List[IndexComposition]:
        query = text("SELECT trade_date, company_name, ticker_symbol, market_cap_rank FROM public.get_index_composition(:trade_date)")
        try:
            result = await session.execute(query,{"trade_date": trade_date})
            rows = result.mappings().all()
        except DBAPIError as exception:
            orig = exception.orig
            error_message = orig.args[0] if orig and orig.args else "Database error"
            raise ApplicationException(error_message, status_code=422) from exception
        results = list()
        for row in rows:
            index_composition = IndexComposition(
                trade_date=row["trade_date"],
                company_name=row["company_name"],
                ticker_symbol=row["ticker_symbol"],
                market_cap_rank=row["market_cap_rank"],
            )
            results.append(index_composition)
        return results


    async def get_composition_changes(self, session: AsyncSession, start_date: date = None, end_date: date = None) -> List[CompositionChange]:
        query = text("SELECT change_date, company_name, ticker_symbol, action FROM get_index_composition_change(:start_date, :end_date)")
        try:
            result = await session.execute(query, {"start_date": start_date, "end_date": end_date})
            rows = result.mappings().all()
        except DBAPIError as exception:
            orig = exception.orig
            error_message = orig.args[0] if orig and orig.args else "Database error"
            raise ApplicationException(error_message, status_code=422) from exception
        results = list()
        for row in rows:
            composition_change = CompositionChange(
                change_date=row["change_date"],
                company_name=row["company_name"],
                ticker_symbol=row["ticker_symbol"],
                action=row["action"]
            )
            results.append(composition_change)
        return results

def get_index_composition_service():
    return IndexCompositionService()