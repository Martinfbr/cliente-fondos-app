from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes import fondos
from app.exceptions import (
    FondoNoEncontradoError,
    MontoInvalidoError,
    SaldoInsuficienteError
)

app = FastAPI(title="API de Fondos de Inversión")

# 👉 Registro de rutas versionadas (ajustado si ya usas /v1)
app.include_router(fondos.router)

# 👉 Manejo de excepciones personalizadas

@app.exception_handler(FondoNoEncontradoError)
async def fondo_no_encontrado_handler(request: Request, exc: FondoNoEncontradoError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )

@app.exception_handler(MontoInvalidoError)
async def monto_invalido_handler(request: Request, exc: MontoInvalidoError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )

@app.exception_handler(SaldoInsuficienteError)
async def saldo_insuficiente_handler(request: Request, exc: SaldoInsuficienteError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )
