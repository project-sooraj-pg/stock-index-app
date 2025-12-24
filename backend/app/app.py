from fastapi import FastAPI, APIRouter

from backend.app.api.v1 import data_export, index_construction, index_retrieval
from backend.app.core.configuration import configuration
from backend.app.core.redis import lifespan

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(index_construction.router, tags=["Index Construction API"])
api_router.include_router(index_retrieval.router, tags=["Index Retrieval API"])
api_router.include_router(data_export.router, tags=["Data Export API"])

app = FastAPI(lifespan=lifespan, title=configuration.app_name)

app.include_router(api_router)