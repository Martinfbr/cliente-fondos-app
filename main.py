from fastapi import FastAPI
from app.routes import fondos

app = FastAPI(title="API de Fondos de Inversión")

# Registrar rutas
app.include_router(fondos.router, prefix="/fondos", tags=["Fondos"])
