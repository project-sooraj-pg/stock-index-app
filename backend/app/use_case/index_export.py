from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.index_composition import IndexCompositionService, get_index_composition_service
from app.service.index_performance import IndexPerformanceService, get_index_performance_service


class IndexExportUseCase:

    def __init__(self, index_performance_service: IndexPerformanceService, index_composition_service: IndexCompositionService):
        self.index_performance_service = index_performance_service
        self.index_composition_service = index_composition_service

    async def build_export_dataset(self, session: AsyncSession):
        index_performances = await self.index_performance_service.get_index_performance(session=session)
        index_compositions = await self.index_composition_service.get_index_composition(session=session)
        composition_changes = await self.index_composition_service.get_composition_changes(session=session)

        return {
            "Index Performance": index_performances,
            "Daily Compositions": index_compositions,
            "Composition Changes": composition_changes,
        }

def get_index_export_use_case(
    index_performance_service: IndexPerformanceService = Depends(get_index_performance_service),
    index_composition_service: IndexCompositionService = Depends(get_index_composition_service),
):
    return IndexExportUseCase(index_performance_service, index_composition_service)
