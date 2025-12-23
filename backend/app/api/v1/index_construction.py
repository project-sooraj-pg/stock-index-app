from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from backend.app.model.param.index_construction import BuildIndexParams
from backend.app.model.response.success_response import SuccessResponse
from backend.app.service.compute import ComputeService, get_compute_service

router = APIRouter()

@router.post("/build_index", response_model=SuccessResponse[str], status_code=status.HTTP_201_CREATED)
async def build_index(
    params: BuildIndexParams = Depends(),
    compute_service: ComputeService = Depends(get_compute_service)
):
    result = await compute_service.build_index(params)
    return JSONResponse(content=SuccessResponse(data=result).model_dump(), status_code=status.HTTP_201_CREATED)
