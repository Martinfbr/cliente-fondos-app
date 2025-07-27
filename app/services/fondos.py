# app/services/fondos.py
from datetime import datetime
import uuid

from app.database.dynamodb import (
    insertar_transaccion,
    obtener_transacciones,
    obtener_fondo_por_id,
    marcar_transaccion_como_cancelada,
)

from app.services.saldo import obtener_saldo, actualizar_saldo
from app.exceptions import FondoNoEncontradoError, SaldoInsuficienteError, MontoInvalidoError


def suscribirse_a_fondo(request):
    fondo_info = obtener_fondo_por_id(request.fondo_id)
    if not fondo_info:
        raise FondoNoEncontradoError(request.fondo_id)

    try:
        monto_minimo = int(fondo_info["MontoMinimo"])
    except (KeyError, ValueError):
        raise ValueError(
            f"El fondo '{fondo_info.get('Nombre', 'Desconocido')}' no tiene definido un monto mínimo válido."
        )

    cliente_id = request.cliente_id
    monto_solicitado = request.monto

    if monto_solicitado < monto_minimo:
        raise MontoInvalidoError(monto_solicitado, monto_minimo, fondo_info["Nombre"])

    saldo_actual = obtener_saldo(cliente_id)
    if saldo_actual < monto_solicitado:
        raise SaldoInsuficienteError(fondo_info["Nombre"], saldo_actual, monto_solicitado)

    transaccion = {
        "transaccion_id": str(uuid.uuid4()),
        "cliente_id": cliente_id,
        "fondo_id": request.fondo_id,
        "fondo_nombre": fondo_info["Nombre"],
        "monto": monto_solicitado,
        "tipo": "apertura",
        "fecha": datetime.utcnow().isoformat(),
        "estado": "activa"
    }

    insertar_transaccion(transaccion)
    nuevo_saldo = saldo_actual - monto_solicitado
    actualizar_saldo(cliente_id, nuevo_saldo)

    return {
        "mensaje": f"✅ Suscripción exitosa al fondo {fondo_info['Nombre']}",
        "saldo_actual": nuevo_saldo
    }

def cancelar_fondo(request):
    fondo_info = obtener_fondo_por_id(request.fondo_id)
    if not fondo_info:
        raise FondoNoEncontradoError(request.fondo_id)

    cliente_id = request.cliente_id
    saldo_actual = obtener_saldo(cliente_id)

    transacciones_cliente = obtener_transacciones(cliente_id)
    transacciones_apertura_activas = [
        t for t in transacciones_cliente
        if t["tipo"] == "apertura"
        and t["fondo_id"] == request.fondo_id
        and t.get("estado", "activa") == "activa"
    ]

    if not transacciones_apertura_activas:
        return {
            "error": f"No hay suscripciones activas al fondo {fondo_info['Nombre']}."
        }

    monto_total_a_devolver = sum(int(t["monto"]) for t in transacciones_apertura_activas)

    transaccion_cancelacion = {
        "transaccion_id": str(uuid.uuid4()),
        "cliente_id": cliente_id,
        "fondo_id": request.fondo_id,
        "fondo_nombre": fondo_info["Nombre"],
        "monto": monto_total_a_devolver,
        "tipo": "cancelacion",
        "fecha": datetime.utcnow().isoformat()
    }
    insertar_transaccion(transaccion_cancelacion)

    for trans in transacciones_apertura_activas:
        marcar_transaccion_como_cancelada(trans["transaccion_id"])

    nuevo_saldo = saldo_actual + monto_total_a_devolver
    actualizar_saldo(cliente_id, nuevo_saldo)

    return {
        "mensaje": f"❌ Cancelación exitosa del fondo {fondo_info['Nombre']}. Se devolvieron ${monto_total_a_devolver}.",
        "saldo_actual": nuevo_saldo
    }

def obtener_historial(cliente_id: str):
    return obtener_transacciones(cliente_id)
