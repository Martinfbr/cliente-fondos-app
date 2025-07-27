# app/exceptions.py
class FondoNoEncontradoError(Exception):
    def __init__(self, fondo_id: str):
        super().__init__(f"Fondo '{fondo_id}' no encontrado.")

class SaldoInsuficienteError(Exception):
    def __init__(self, fondo_nombre: str):
        super().__init__(f"No tiene saldo suficiente para vincularse al fondo '{fondo_nombre}'.")

class MontoInvalidoError(Exception):
    def __init__(self, monto: int, minimo: int, fondo_nombre: str):
        super().__init__(f"El monto ingresado ({monto}) es inferior al mínimo requerido ({minimo}) para el fondo '{fondo_nombre}'.")
