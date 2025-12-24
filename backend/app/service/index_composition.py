from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

class IndexCompositionService:

    async def get_index_composition(self, session: AsyncSession, trade_date: date = None):
        pass

    async def get_composition_changes(self, session: AsyncSession, start_date: date = None, end_date: date = None):
        pass

def get_index_composition_service():
    return IndexCompositionService()