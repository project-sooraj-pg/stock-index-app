from io import BytesIO

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.store.database import get_database

from app.use_case.index_export import IndexExportUseCase, get_index_export_use_case
from app.util.excel_exporter import ExcelExporter, get_excel_exporter

router = APIRouter()

@router.post("/export-data")
async def export_data(
        index_export_use_case: IndexExportUseCase = Depends(get_index_export_use_case),
        exporter: ExcelExporter = Depends(get_excel_exporter),
        session: AsyncSession = Depends(get_database)):

    dataset = await index_export_use_case.build_export_dataset(session=session)
    output = BytesIO()
    await exporter.export(dataset=dataset, output=output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=index_export.xlsx"},
    )
