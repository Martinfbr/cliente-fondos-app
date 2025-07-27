import uuid
from datetime import datetime
from app.database.dynamodb import insertar_transaccion

# Datos de prueba
transaccion = {
    'transaccion_id': str(uuid.uuid4()),  # Identificador único
    'fondo_id': '2',
    'tipo': 'apertura',
    'monto': 125000,
    'fecha': datetime.utcnow().isoformat()
}

# Ejecutar la inserción
try:
    insertar_transaccion(transaccion)
    print("✅ Transacción insertada correctamente.")
except Exception as e:
    print(f"❌ Error al insertar transacción: {e}")
