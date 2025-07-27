from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Transaccion(BaseModel):
    transaccion_id: str
    tipo: Literal["apertura", "cancelacion"]
    fondo_id: str
    fondo_nombre: str
    monto: int
    fecha: datetime
