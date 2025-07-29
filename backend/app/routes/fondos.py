# app/routes/fondos.py
from fastapi import APIRouter
from app.services import dynamodb_service

router = APIRouter(prefix="/fondos", tags=["Fondos"])

@router.get("/")
def listar_fondos():
    """
    Retorna todos los fondos disponibles en la tabla Fondos.
    """
    fondos = dynamodb_service.obtener_todos_fondos()
    return {"fondos": fondos}
