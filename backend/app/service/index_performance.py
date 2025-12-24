from datetime import date
from typing import List

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import ApplicationException
from app.model.core.index_performance import IndexPerformance


class IndexPerformanceService:

    async def get_index_performance(self, session: AsyncSession, start_date: date = None, end_date: date = None) -> List[IndexPerformance]:
        trade_date: date
        index_value: float
        daily_return_in_percentage: float
        cumulative_return_in_percentage: float

        query = text("SELECT trade_date, index_value, daily_return_in_percentage, cumulative_return_in_percentage FROM public.get_index_performance(:start_date, :end_date)")
        try:
            result = await session.execute(query, {"start_date": start_date, "end_date": end_date})
            rows = result.mappings().all()
        except DBAPIError as exception:
            orig = exception.orig
            error_message = orig.args[0] if orig and orig.args else "Database error"
            raise ApplicationException(error_message, status_code=422) from exception
        results = list()
        for row in rows:
            index_performance = IndexPerformance(
                trade_date=row["trade_date"],
                index_value=row["index_value"],
                daily_return_in_percentage=row["daily_return_in_percentage"],
                cumulative_return_in_percentage=row["cumulative_return_in_percentage"],
            )
            results.append(index_performance)
        return results

def get_index_performance_service():
    return IndexPerformanceService()