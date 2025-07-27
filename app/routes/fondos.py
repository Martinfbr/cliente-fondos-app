from fastapi import APIRouter
from app.models.schemas import SuscripcionRequest, CancelacionRequest
from app.services import fondos

router = APIRouter()

@router.post("/suscribirse")
def suscribirse(request: SuscripcionRequest):
    return fondos.suscribirse_a_fondo(request)

@router.post("/cancelar")
def cancelar(request: CancelacionRequest):
    return fondos.cancelar_fondo(request)

@router.get("/historial/{cliente_id}")
def historial(cliente_id: str):
    return fondos.obtener_historial(cliente_id)
