from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.dto.composition_change import CompositionChange
from backend.app.model.core.index_composition import IndexComposition
from backend.app.model.core.index_performance import IndexPerformance
from backend.app.model.param.index_retrieval import IndexPerformanceParams, IndexCompositionParams, CompositionChangesParams
from backend.app.model.response.success_response import SuccessResponse
from backend.app.service.index_composition import IndexCompositionService, get_index_composition_service
from backend.app.service.index_performance import IndexPerformanceService, get_index_performance_service
from backend.app.store.database import get_database

router = APIRouter()

@router.get("/index-performance", response_model=SuccessResponse[List[IndexPerformance]])
async def get_index_performance(
    params: IndexPerformanceParams = Depends(),
    index_performance_service: IndexPerformanceService = Depends(get_index_performance_service),
    session: AsyncSession = Depends(get_database)
):
    result = await index_performance_service.get_index_performance(session=session, start_date=params.start_date, end_date=params.end_date)
    return JSONResponse(content=SuccessResponse(data=result).model_dump())

@router.get("/index-composition", response_model=SuccessResponse[IndexComposition])
async def get_index_composition(
    params: IndexCompositionParams = Depends(),
    index_composition_service: IndexCompositionService = Depends(get_index_composition_service),
    session: AsyncSession = Depends(get_database)
):
    result = await index_composition_service.get_index_composition(session=session, trade_date=params.trade_date)
    return JSONResponse(content=SuccessResponse(data=result).model_dump())

@router.get("/composition-changes", response_model=SuccessResponse[List[CompositionChange]])
async def get_composition_changes(
    params: CompositionChangesParams = Depends(),
    index_composition_service: IndexCompositionService = Depends(get_index_composition_service),
    session: AsyncSession = Depends(get_database)
):
    result = await index_composition_service.get_composition_changes(session=session, start_date=params.start_date, end_date=params.end_date)
    return JSONResponse(content=SuccessResponse(data=result).model_dump())
