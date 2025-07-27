from fastapi import APIRouter, Depends
from app.models.schemas import SuscripcionRequest, CancelacionRequest
from app.services import fondos
from app.database.dynamodb import obtener_transacciones
from app.dependencies.auth import verificar_api_key  # ✅ Nombre correcto de la función

router = APIRouter(
    prefix="/v1/fondos",  # ✅ Versión de la API
    tags=["Fondos"],
    dependencies=[Depends(verificar_api_key)]  # ✅ Protección con API Key
)

@router.post("/suscribirse")
def suscribirse(request: SuscripcionRequest):
    return fondos.suscribirse_a_fondo(request)

@router.post("/cancelar")
def cancelar(request: CancelacionRequest):
    return fondos.cancelar_fondo(request)

@router.get("/historial/{cliente_id}")
def obtener_historial(cliente_id: str):
    transacciones = obtener_transacciones(cliente_id)

    if not transacciones:
        return {"mensaje": f"No hay historial de transacciones para el cliente '{cliente_id}'."}

    return transacciones
