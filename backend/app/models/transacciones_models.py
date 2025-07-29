from pydantic import BaseModel

class SuscribirInput(BaseModel):
    user_id: str
    fondo_id: str
    monto: int

class CancelarInput(BaseModel):
    user_id: str
    fondo_id: str

class TransaccionResponse(BaseModel):
    status: str
    message: str

class HistorialResponse(BaseModel):
    transacciones: list
