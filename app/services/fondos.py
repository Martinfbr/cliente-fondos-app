from app.database.dynamodb import (
    insertar_transaccion,
    obtener_transacciones,
    obtener_fondo_por_id, # Usamos ID en vez de Nombre
    obtener_transacciones_apertura 
)
from app.services.saldo import obtener_saldo, actualizar_saldo
import uuid
from datetime import datetime
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError, MontoInvalidoError


# 👉 Función para suscribirse a un fondo de inversión
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError, MontoInvalidoError

def suscribirse_a_fondo(request):
    fondo_info = obtener_fondo_por_id(request.fondo_id)
    if not fondo_info:
        raise FondoNoEncontradoError(request.fondo_id)

    monto_minimo = int(fondo_info["MontoMinimo"])
    cliente_id = request.cliente_id
    monto_solicitado = request.monto

    if monto_solicitado < monto_minimo:
        raise MontoInvalidoError(monto_solicitado, monto_minimo, fondo_info['Nombre'])

    saldo_actual = obtener_saldo(cliente_id)

    if saldo_actual < monto_solicitado:
        raise SaldoInsuficienteError(fondo_info['Nombre'])

    transaccion = {
        "transaccion_id": str(uuid.uuid4()),
        "cliente_id": cliente_id,
        "fondo_id": request.fondo_id,
        "fondo_nombre": fondo_info['Nombre'],
        "monto": monto_solicitado,
        "tipo": "apertura",
        "fecha": datetime.utcnow().isoformat()
    }

    insertar_transaccion(transaccion)
    nuevo_saldo = saldo_actual - monto_solicitado
    actualizar_saldo(cliente_id, nuevo_saldo)

    return {
        "mensaje": f"✅ Suscripción exitosa al fondo {fondo_info['Nombre']}",
        "saldo_actual": nuevo_saldo
    }

# 👉 Función para cancelar una suscripción a fondo
def cancelar_fondo(request):
    fondo_info = obtener_fondo_por_id(request.fondo_id)
    if not fondo_info:
        return {"error": f"Fondo '{request.fondo_id}' no encontrado."}

    cliente_id = request.cliente_id

    # 🔍 Obtener todas las transacciones de apertura del fondo para este cliente
    transacciones_apertura = obtener_transacciones_apertura(cliente_id, request.fondo_id)

    if not transacciones_apertura:
        return {"error": f"No se encontraron suscripciones activas al fondo {fondo_info['Nombre']}"}

    # ➕ Sumar los montos de todas las aperturas
    monto_total_apertura = sum(int(tx['monto']) for tx in transacciones_apertura)

    # 🔁 Reintegrar el monto al saldo del cliente
    saldo_actual = obtener_saldo(cliente_id)
    nuevo_saldo = saldo_actual + monto_total_apertura
    actualizar_saldo(cliente_id, nuevo_saldo)

    # 📝 Registrar transacción de cancelación
    transaccion = {
        "transaccion_id": str(uuid.uuid4()),
        "cliente_id": cliente_id,
        "fondo_id": request.fondo_id,
        "fondo_nombre": fondo_info['Nombre'],
        "monto": monto_total_apertura,
        "tipo": "cancelacion",
        "fecha": datetime.utcnow().isoformat()
    }

    insertar_transaccion(transaccion)

    return {
        "mensaje": f"❌ Cancelación exitosa del fondo {fondo_info['Nombre']}. Se devolvieron ${monto_total_apertura}.",
        "saldo_actual": nuevo_saldo
    }

# 👉 Función para consultar el historial de transacciones de un cliente
def obtener_historial(cliente_id: str):
    return obtener_transacciones(cliente_id)
