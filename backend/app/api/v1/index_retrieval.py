from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.core.index_composition import IndexComposition
from app.model.core.index_performance import IndexPerformance
from app.model.dto.composition_change import CompositionChangeDto
from app.model.param.index_retrieval import IndexPerformanceParams, IndexCompositionParams, CompositionChangesParams
from app.store.database import get_database
from app.use_case.index_retrieval import IndexRetrievalUseCase, get_index_retrieval_use_case

router = APIRouter()

@router.get("/index-performance", response_model=List[IndexPerformance])
async def get_index_performance(
    params: IndexPerformanceParams = Depends(),
    index_retrieval_use_case: IndexRetrievalUseCase = Depends(get_index_retrieval_use_case),
    session: AsyncSession = Depends(get_database)
):
    return await index_retrieval_use_case.get_index_performance(session=session, params=params)

@router.get("/index-composition", response_model=List[IndexComposition])
async def get_index_composition(
    params: IndexCompositionParams = Depends(),
    index_retrieval_use_case: IndexRetrievalUseCase = Depends(get_index_retrieval_use_case),
    session: AsyncSession = Depends(get_database)
):
    return await index_retrieval_use_case.get_index_composition(session=session, params=params)

@router.get("/composition-changes", response_model=List[CompositionChangeDto])
async def get_composition_changes(
    params: CompositionChangesParams = Depends(),
    index_retrieval_use_case: IndexRetrievalUseCase = Depends(get_index_retrieval_use_case),
    session: AsyncSession = Depends(get_database)
):
    return await index_retrieval_use_case.get_composition_changes(session=session, params=params)
