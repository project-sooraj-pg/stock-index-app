from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.app.model.core.composition_change import CompositionChange
from backend.app.model.core.index_composition import IndexComposition
from backend.app.model.core.index_performance import IndexPerformance
from backend.app.model.param.index_retrieval import IndexPerformanceParams, IndexCompositionParams, CompositionChangesParams
from backend.app.model.response.success_response import SuccessResponse
from backend.app.service.compute import ComputeService, get_compute_service

router = APIRouter()

@router.get("/index-performance", response_model=SuccessResponse[List[IndexPerformance]])
async def get_index_performance(
    params: IndexPerformanceParams = Depends(),
    compute_service: ComputeService = Depends(get_compute_service)
):
    result = await compute_service.get_index_performance(params)
    return JSONResponse(content=SuccessResponse(data=result).model_dump())

@router.get("/index-composition", response_model=SuccessResponse[IndexComposition])
async def get_index_composition(
    params: IndexCompositionParams = Depends(),
    compute_service: ComputeService = Depends(get_compute_service)
):
    result = await compute_service.get_index_composition(params)
    return JSONResponse(content=SuccessResponse(data=result).model_dump())

@router.get("/composition-changes", response_model=SuccessResponse[List[CompositionChange]])
async def get_composition_changes(
    params: CompositionChangesParams = Depends(),
    compute_service: ComputeService = Depends(get_compute_service)
):
    result = await compute_service.get_composition_changes(params)
    return JSONResponse(content=SuccessResponse(data=result).model_dump())
