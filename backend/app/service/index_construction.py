from datetime import date

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.configuration import configuration


class IndexConstructionService:

    async def build_index(self, session: AsyncSession, start_date: date = None, end_date: date = None) -> None:
        async with session.begin():
            # compute index daily constituents
            status, message = await self._call_database_function(
                session,
                "compute_index_daily_constituent",
                configuration.total_number_of_index_constituents,
                start_date,
                end_date,
            )
            if status != "SUCCESS":
                raise RuntimeError(f"Unable to build index: {message}")
            # compute index daily performance
            status, message = await self._call_database_function(
                session,
                "compute_index_daily_performance",
                configuration.index_base_value
            )
            if status != "SUCCESS":
                raise RuntimeError(f"Index computation failed: {message}")
        return

    async def _call_database_function(self, session: AsyncSession, function_name: str, *args) -> tuple[str, str]:
        """Method to execute stored procedure"""
        placeholders = ", ".join(f":p{i}" for i in range(len(args)))
        query = text(f"""SELECT status, message FROM {function_name}({placeholders})""")
        params = {f"p{i}": arg for i, arg in enumerate(args)}
        result = await session.execute(query, params)
        row = result.fetchone()
        if row is None:
            raise RuntimeError(f"{function_name} returned no result")
        return row.status, row.message

def get_index_construction_service():
    return IndexConstructionService()