from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.param.index_construction import BuildIndexParams
from backend.app.store.database import get_database
from backend.app.use_case.index_construction import IndexConstructionUseCase, get_index_construction_use_case

router = APIRouter()

@router.post("/build_index", status_code=status.HTTP_201_CREATED)
async def build_index(
    params: BuildIndexParams = Depends(),
    index_construction_use_case: IndexConstructionUseCase = Depends(get_index_construction_use_case),
    session: AsyncSession = Depends(get_database)
):
    await index_construction_use_case.build_index(session=session, params=params)
    return JSONResponse(content=None, status_code=status.HTTP_201_CREATED)
