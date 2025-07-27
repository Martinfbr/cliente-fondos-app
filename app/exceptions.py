# app/exceptions.py

class FondoNoEncontradoError(Exception):
    def __init__(self, fondo_id: str):
        self.fondo_id = fondo_id
        self.message = f"❌ Fondo con ID '{fondo_id}' no encontrado."
        super().__init__(self.message)


class SaldoInsuficienteError(Exception):
    def __init__(self, fondo_nombre: str, saldo_disponible: int = None, monto_requerido: int = None):
        self.fondo_nombre = fondo_nombre
        self.saldo_disponible = saldo_disponible
        self.monto_requerido = monto_requerido

        mensaje_base = f"❌ No tiene saldo suficiente para vincularse al fondo '{fondo_nombre}'."
        if saldo_disponible is not None and monto_requerido is not None:
            mensaje_base += f" Saldo actual: ${saldo_disponible}, requerido: ${monto_requerido}."
        
        self.message = mensaje_base
        super().__init__(self.message)


class MontoInvalidoError(Exception):
    def __init__(self, monto: int, minimo: int, fondo_nombre: str):
        self.monto = monto
        self.minimo = minimo
        self.fondo_nombre = fondo_nombre

        self.message = (
            f"❌ El monto ingresado (${monto}) es inferior al mínimo requerido (${minimo}) "
            f"para el fondo '{fondo_nombre}'."
        )
        super().__init__(self.message)
