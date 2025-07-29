from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

# Excepción personalizada
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

# Handler para AppException
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.message},
    )

# Handler para ClientError (DynamoDB u otros servicios AWS)
async def dynamodb_exception_handler(request: Request, exc: ClientError):
    error_msg = exc.response["Error"]["Message"]
    logger.error(f"DynamoDB Error: {error_msg}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": f"Error en base de datos: {error_msg}"},
    )

# Handler para HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

# Handler genérico para errores no controlados
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Error interno del servidor"},
    )
