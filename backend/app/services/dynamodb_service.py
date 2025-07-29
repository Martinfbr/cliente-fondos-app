import boto3
import uuid
import os
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from app.utils.exceptions import AppException  # <- nuestra excepción personalizada

# Conexión a DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
sns_client = boto3.client("sns", region_name="us-east-2")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

fondos_table = dynamodb.Table("Fondos")
usuario_saldo_table = dynamodb.Table("UsuarioSaldo")
transacciones_table = dynamodb.Table("Transacciones")


# SUSCRIBIR
def suscribir_a_fondo(user_id: str, fondo_id: str, monto: int):
    try:
        # 1. Obtener fondo
        fondo = fondos_table.get_item(Key={"FondoId": fondo_id}).get("Item")
        if not fondo:
            raise AppException(f"Fondo {fondo_id} no encontrado", status_code=404)

        monto_minimo = int(fondo["MontoMinimo"])
        nombre_fondo = fondo["Nombre"]

        # 2. Validar monto mínimo
        if monto < monto_minimo:
            raise AppException(
                f"El monto ingresado es menor al mínimo requerido ({monto_minimo}).",
                status_code=400
            )

        # 3. Validar usuario
        usuario = usuario_saldo_table.get_item(Key={"user_id": user_id}).get("Item")
        if not usuario:
            raise AppException(f"Usuario {user_id} no encontrado", status_code=404)

        saldo_actual = int(usuario["saldo"])
        metodo_notificacion = usuario.get("metodo_notificacion")
        contacto = usuario.get("contacto")

        # 4. Validar saldo suficiente
        if saldo_actual < monto:
            raise AppException(f"No tiene saldo disponible para el fondo {nombre_fondo}", 400)

        # 5. Restar saldo
        nuevo_saldo = saldo_actual - monto
        usuario_saldo_table.update_item(
            Key={"user_id": user_id},
            UpdateExpression="SET saldo = :nuevo",
            ExpressionAttributeValues={":nuevo": nuevo_saldo}
        )

        # 6. Crear transacción
        transaccion_id = str(uuid.uuid4())
        fecha_actual = datetime.now(timezone.utc).isoformat()

        transacciones_table.put_item(Item={
            "transaccion_id": transaccion_id,
            "user_id": user_id,
            "fondo_id": fondo_id,
            "tipo": "suscripcion",
            "monto": monto,
            "estado": "activo",
            "fecha": fecha_actual
        })

        # 7. Notificación
        if metodo_notificacion and contacto:
            mensaje = f"Te has suscrito al fondo {nombre_fondo} por {monto} COP el {fecha_actual}."
            enviar_notificacion(metodo_notificacion, contacto, mensaje)

        return {
            "status": "success",
            "message": f"Suscripción exitosa a {nombre_fondo} por {monto} COP.",
            "transaccion_id": transaccion_id,
            "saldo_actual": nuevo_saldo
        }

    except ClientError as e:
        raise AppException(f"Error DynamoDB: {e.response['Error']['Message']}", status_code=500)


# CANCELAR
def cancelar_suscripcion(cliente_id: str, fondo_id: str):
    try:
        resp = transacciones_table.scan(
            FilterExpression=Attr('user_id').eq(cliente_id) &
                             Attr('fondo_id').eq(fondo_id) &
                             Attr('estado').eq('activo') &
                             Attr('tipo').eq('suscripcion')
        )

        transacciones_activas = resp['Items']

        if not transacciones_activas:
            raise AppException("No existe suscripción activa para este fondo.", 404)

        total_reintegro = sum(t['monto'] for t in transacciones_activas)

        # Cancelar transacciones activas
        for transaccion in transacciones_activas:
            transacciones_table.update_item(
                Key={'transaccion_id': transaccion['transaccion_id']},
                UpdateExpression="SET estado = :e",
                ExpressionAttributeValues={':e': 'cancelado'}
            )

        # Actualizar saldo
        saldo_data = usuario_saldo_table.get_item(Key={'user_id': cliente_id}).get('Item')
        nuevo_saldo = saldo_data['saldo'] + total_reintegro
        usuario_saldo_table.update_item(
            Key={'user_id': cliente_id},
            UpdateExpression="SET saldo = :s",
            ExpressionAttributeValues={':s': nuevo_saldo}
        )

        # Registrar transacción cancelación
        transaccion_id = str(uuid.uuid4())
        fecha_actual = datetime.now(timezone.utc).isoformat()

        transacciones_table.put_item(Item={
            "transaccion_id": transaccion_id,
            "user_id": cliente_id,
            "fondo_id": fondo_id,
            "tipo": "cancelacion",
            "monto": total_reintegro,
            "estado": "completado",
            "fecha": fecha_actual
        })

        # Notificación
        usuario = usuario_saldo_table.get_item(Key={"user_id": cliente_id}).get("Item")
        metodo_notificacion = usuario.get("metodo_notificacion")
        contacto = usuario.get("contacto")

        if metodo_notificacion and contacto:
            mensaje = (
                f"Has cancelado tu suscripción al fondo {fondo_id}. "
                f"Se reintegraron {total_reintegro} COP el {fecha_actual}."
            )
            enviar_notificacion(metodo_notificacion, contacto, mensaje)

        return {
            "status": "success",
            "message": f"Suscripciones canceladas y {total_reintegro} COP reintegrados",
            "nuevo_saldo": nuevo_saldo
        }

    except ClientError as e:
        raise AppException(f"Error DynamoDB: {e.response['Error']['Message']}", 500)


# HISTORIAL
def obtener_historial(cliente_id: str):
    try:
        resp = transacciones_table.scan(
            FilterExpression=Attr('user_id').eq(cliente_id)
        )
        transacciones = resp.get("Items", [])

        transacciones_ordenadas = sorted(transacciones, key=lambda x: x["fecha"], reverse=True)

        return {"transacciones": transacciones_ordenadas}

    except ClientError as e:
        raise AppException(f"Error DynamoDB: {e.response['Error']['Message']}", 500)


# SNS
def enviar_notificacion(metodo: str, contacto: str, mensaje: str):
    if not SNS_TOPIC_ARN:
        raise AppException("SNS_TOPIC_ARN no configurado", 500)

    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f"[{metodo.upper()}] {mensaje} -> Contacto: {contacto}",
        Subject="Notificación Fondo"
    )
