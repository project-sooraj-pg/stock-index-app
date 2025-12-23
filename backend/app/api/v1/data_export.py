from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from backend.app.model.response.success_response import SuccessResponse
from backend.app.service.export import ExportService, get_export_service

router = APIRouter()

@router.post("/export-data", response_model=SuccessResponse[str], status_code=status.HTTP_201_CREATED)
async def export_data(export_service: ExportService = Depends(get_export_service)):
    result = await export_service.export_data()
    return JSONResponse(content=SuccessResponse(data=result).model_dump(), status_code=status.HTTP_201_CREATED)
