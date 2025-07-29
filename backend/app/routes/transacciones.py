from fastapi import APIRouter
from app.models.transacciones_models import SuscribirInput, CancelarInput
from app.services.dynamodb_service import (
    suscribir_a_fondo,
    cancelar_suscripcion,
    obtener_historial
)

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/suscribir")
def suscribir(input_data: SuscribirInput):
    return suscribir_a_fondo(
        user_id=input_data.user_id,
        fondo_id=input_data.fondo_id,
        monto=input_data.monto
    )

@router.post("/cancelar")
def cancelar(input_data: CancelarInput):
    return cancelar_suscripcion(
        cliente_id=input_data.user_id,
        fondo_id=input_data.fondo_id
    )

@router.get("/historial/{cliente_id}")
def historial(cliente_id: str):
    return obtener_historial(cliente_id)
