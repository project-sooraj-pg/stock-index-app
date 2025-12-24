from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.param.index_construction import BuildIndexParams
from backend.app.model.response.success_response import SuccessResponse
from backend.app.service.index_construction import IndexConstructionService, get_index_construction_service
from backend.app.store.database import get_database

router = APIRouter()

@router.post("/build_index", response_model=SuccessResponse[str], status_code=status.HTTP_201_CREATED)
async def build_index(
    params: BuildIndexParams = Depends(),
    index_construction_service: IndexConstructionService = Depends(get_index_construction_service),
    session: AsyncSession = Depends(get_database)
):
    result = await index_construction_service.build_index(session=session, start_date=params.start_date, end_date=params.end_date)
    return JSONResponse(content=SuccessResponse(result=result).model_dump(), status_code=status.HTTP_201_CREATED)
