from collections import defaultdict
from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_cache
from app.model.core.composition_change import CompositionChange
from app.model.core.index_composition import IndexComposition
from app.model.core.index_performance import IndexPerformance
from app.model.dto.composition_change import CompositionChangeDto, CompanyTicker
from app.model.param.index_retrieval import IndexPerformanceParams, IndexCompositionParams, CompositionChangesParams
from app.service.index_composition import IndexCompositionService, get_index_composition_service
from app.service.index_performance import IndexPerformanceService, get_index_performance_service


class IndexRetrievalUseCase:
    def __init__(self, index_performance_service: IndexPerformanceService, index_composition_service: IndexCompositionService):
        self.index_performance_service = index_performance_service
        self.index_composition_service = index_composition_service

    @redis_cache(ttl=60)
    async def get_index_performance(self, session: AsyncSession, params: IndexPerformanceParams) ->List[IndexPerformance]:
        start_date = params.start_date
        end_date = params.end_date
        return await self.index_performance_service.get_index_performance(session=session, start_date=start_date, end_date=end_date)

    @redis_cache(ttl=60)
    async def get_index_composition(self, session: AsyncSession, params: IndexCompositionParams) -> List[IndexComposition]:
        trade_date = params.trade_date
        return await self.index_composition_service.get_index_composition(session=session, trade_date=trade_date)

    @redis_cache(ttl=60)
    async def get_composition_changes(self, session: AsyncSession, params: CompositionChangesParams) -> List[CompositionChangeDto]:
        start_date = params.start_date
        end_date = params.end_date
        composition_changes = await self.index_composition_service.get_composition_changes(session=session, start_date=start_date, end_date=end_date)
        return self._convert_composition_changes_to_composition_change_dtos(composition_changes)

    def _convert_composition_changes_to_composition_change_dtos(self, composition_changes: List[CompositionChange]) -> List[CompositionChangeDto]:
        grouped = defaultdict(lambda: {"added": [], "removed": []})
        for composition_change in composition_changes:
            company_ticker = CompanyTicker(
                company_name=composition_change.company_name,
                ticker_symbol=composition_change.ticker_symbol
            )
            if composition_change.action.lower() == "added":
                grouped[composition_change.change_date]["added"].append(company_ticker)
            elif composition_change.action.lower() == "removed":
                grouped[composition_change.change_date]["removed"].append(company_ticker)
            else:
                raise ValueError(f"Unknown action '{composition_change.action}' in CompositionChange")
        composition_change_dtos = list()
        for change_date, data in sorted(grouped.items()):
            composition_change_dto = CompositionChangeDto(change_date=change_date, added=data["added"], removed=data["removed"])
            composition_change_dtos.append(composition_change_dto)
        return composition_change_dtos

def get_index_retrieval_use_case(
    index_performance_service: IndexPerformanceService = Depends(get_index_performance_service),
    index_composition_service: IndexCompositionService = Depends(get_index_composition_service),
):
    return IndexRetrievalUseCase(index_performance_service, index_composition_service)
