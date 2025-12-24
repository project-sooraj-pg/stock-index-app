from io import BytesIO

from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from backend.app.model.response.success_response import SuccessResponse

from backend.app.use_case.index_export import IndexExportUseCase, get_index_export_use_case
from backend.app.util.excel_exporter import ExcelExporter, get_excel_exporter

router = APIRouter()

@router.post("/export-data", response_model=SuccessResponse[str])
async def export_data(
        use_case: IndexExportUseCase = Depends(get_index_export_use_case),
        exporter: ExcelExporter = Depends(get_excel_exporter)):

    dataset = await use_case.build_export_dataset()
    output = BytesIO()
    await exporter.export(dataset=dataset, output=output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=index_export.xlsx"},
    )
