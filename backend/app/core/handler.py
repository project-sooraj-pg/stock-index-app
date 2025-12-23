from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from backend.app.core.exception import AppException

logger = logging.get_logger(__name__)


def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"{exc.message} | path={request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.message
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "message": "Validation failed",
                    "details": exc.errors()
                }
            }
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "message": "Internal server error"
                }
            }
        )