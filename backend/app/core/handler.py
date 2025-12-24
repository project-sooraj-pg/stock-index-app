from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exception import ApplicationException


def register_exception_handlers(app):
    @app.exception_handler(ApplicationException)
    async def app_exception_handler(request: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.message
                }
            }
        )