from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

class IndexPerformanceService:

    async def get_index_performance(self, session: AsyncSession, start_date: date = None, end_date: date = None):
        pass

def get_index_performance_service():
    return IndexPerformanceService()