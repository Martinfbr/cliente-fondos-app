from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routes.transacciones import router as transacciones_router
import os

# IMPORTA LOS HANDLERS Y EXCEPCIONES
from app.utils.exceptions import (
    AppException,
    app_exception_handler,
    dynamodb_exception_handler,
    http_exception_handler,
    generic_exception_handler
)
from botocore.exceptions import ClientError
from fastapi.exceptions import HTTPException

# Detectar si estamos en Lambda
IS_LAMBDA = "AWS_LAMBDA_FUNCTION_NAME" in os.environ

# Configurar root_path solo cuando estemos en Lambda
root_path = "/Prod" if IS_LAMBDA else ""

# Crear la app
app = FastAPI(
    title="API Proyecto App",
    description="API desplegada en AWS Lambda + API Gateway usando FastAPI",
    version="1.0.0",
    root_path=root_path
)

# Registrar handlers globales
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ClientError, dynamodb_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod deberías filtrar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(transacciones_router)

# ------------------- RUTAS DE PRUEBA -------------------
@app.get("/")
def root():
    return {"message": "API funcionando en Lambda + API Gateway"}

@app.get("/test")
def test():
    return {"status": "ok", "message": "Ruta de prueba funcionando"}

@app.get("/contest")
def contest():
    return {"status": "ok", "message": "Ruta contest funcionando"}

# Handler Lambda
handler = Mangum(app)
