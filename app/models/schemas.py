from pydantic import BaseModel

class SuscripcionRequest(BaseModel):
    cliente_id: str
    fondo_id: str
    monto: int 

class CancelacionRequest(BaseModel):
    cliente_id: str
    fondo_id: str
