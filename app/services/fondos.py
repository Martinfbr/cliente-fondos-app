from app.database.dynamodb import (
    insertar_transaccion,
    obtener_transacciones,
    obtener_fondo_por_id, # Usamos ID en vez de Nombre
    obtener_transacciones_apertura 
)
from app.services.saldo import obtener_saldo, actualizar_saldo
import uuid
from datetime import datetime

# 👉 Función para suscribirse a un fondo de inversión
def suscribirse_a_fondo(request):
    fondo_info = obtener_fondo_por_id(request.fondo_id)  # Usamos ID correctamente
    if not fondo_info:
        return {"error": f"Fondo '{request.fondo_id}' no encontrado."}

    monto_minimo = int(fondo_info["MontoMinimo"])
    cliente_id = request.cliente_id
    monto_ingresado = request.monto  # ✅ Este monto lo proporciona el usuario

    # Validar que el monto sea suficiente
    if monto_ingresado < monto_minimo:
        return {
            "error": f"El monto ingresado (${monto_ingresado}) es menor al mínimo requerido (${monto_minimo}) para el fondo '{fondo_info['Nombre']}'."
        }

    saldo_actual = obtener_saldo(cliente_id)

    # Validar que tenga suficiente saldo
    if saldo_actual < monto_ingresado:
        return {
            "error": f"Saldo insuficiente. Tiene ${saldo_actual} y desea suscribirse con ${monto_ingresado}."
        }

    # Registrar la transacción
    transaccion = {
        "transaccion_id": str(uuid.uuid4()),
        "cliente_id": cliente_id,
        "fondo_id": request.fondo_id,
        "fondo_nombre": fondo_info['Nombre'],
        "monto": monto_ingresado,  # ✅ Se guarda el monto real, no el mínimo
        "tipo": "apertura",
        "fecha": datetime.utcnow().isoformat()
    }

    insertar_transaccion(transaccion)

    # Actualizar saldo del cliente
    nuevo_saldo = saldo_actual - monto_ingresado
    actualizar_saldo(cliente_id, nuevo_saldo)

    return {
        "mensaje": f"✅ Suscripción exitosa al fondo {fondo_info['Nombre']} por ${monto_ingresado}",
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
