# main.py
from fastapi import FastAPI
from app.routes import fondos
from app.exceptions import FondoNoEncontradoError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(FondoNoEncontradoError)
async def fondo_no_encontrado_handler(request, exc: FondoNoEncontradoError):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)}
    )

app.include_router(fondos.router)