from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.param.index_construction import BuildIndexParams
from app.service.index_construction import IndexConstructionService, get_index_construction_service


class IndexConstructionUseCase:

    def __init__(self, index_construction_service: IndexConstructionService):
        self.index_construction_service = index_construction_service

    async def build_index(self, session: AsyncSession, params: BuildIndexParams) -> None:
        start_date = params.start_date
        end_date = params.end_date
        return await self.index_construction_service.build_index(session=session, start_date=start_date, end_date=end_date)

def get_index_construction_use_case(index_construction_service: IndexConstructionService = Depends(get_index_construction_service)):
    return IndexConstructionUseCase(index_construction_service)