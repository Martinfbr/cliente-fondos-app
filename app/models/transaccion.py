from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class Transaccion(BaseModel):
    transaccion_id: str
    tipo: Literal["apertura", "cancelacion"]
    estado: str
    fondo_id: str
    fondo_nombre: str
    monto: int
    fecha: datetime  # Pydantic 2 convierte strings ISO automáticamente a datetime
