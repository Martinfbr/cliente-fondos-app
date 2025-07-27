import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Attr
from app.models.transaccion import Transaccion
from datetime import datetime
import uuid

# 🔄 Cargar variables de entorno
load_dotenv()

# 🔧 Cliente de bajo nivel
client = boto3.client(
    'dynamodb',
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# 🔧 Cliente de alto nivel (orientado a objetos)
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Nombres de tablas
TABLE_TRANSACCIONES = 'Transacciones'
TABLE_FONDOS = 'Fondos'
TABLE_USUARIO_SALDO = 'UsuarioSaldo'

# ✅ Insertar transacción
def insertar_transaccion(transaccion: dict):
    try:
        print("📤 Insertando transacción:", transaccion)

        # Si no viene definido el estado, lo asignamos como "activa"
        estado = transaccion.get('estado', 'activo')

        item = {
            'transaccion_id': {'S': transaccion['transaccion_id']},
            'cliente_id': {'S': transaccion['cliente_id']},
            'tipo': {'S': transaccion['tipo']},
            'fondo_id': {'S': transaccion['fondo_id']},
            'fondo_nombre': {'S': transaccion['fondo_nombre']},
            'monto': {'N': str(transaccion['monto'])},
            'fecha': {'S': transaccion['fecha']},
            'estado': {'S': estado}  # ✅ Siempre presente
        }

        client.put_item(TableName=TABLE_TRANSACCIONES, Item=item)
        print("✅ Transacción insertada correctamente.")
    except ClientError as e:
        raise Exception(f"❌ Error al insertar transacción: {e.response['Error']['Message']}")


def obtener_transacciones_apertura_activas(cliente_id, fondo_id):
    transacciones = obtener_transacciones(cliente_id)
    return [
        t for t in transacciones
        if t["tipo"] == "apertura" and t["fondo_id"] == fondo_id and t.get("estado", "activa") == "activa"
    ]

def marcar_transaccion_como_cancelada(transaccion_id):
    tabla = dynamodb.Table("Transacciones")
    tabla.update_item(
        Key={"transaccion_id": transaccion_id},
        UpdateExpression="SET estado = :estado",
        ExpressionAttributeValues={":estado": "cancelada"}
    )

# ✅ Obtener historial de transacciones de un cliente
def obtener_transacciones(cliente_id: str):
    try:
        response = client.scan(
            TableName=TABLE_TRANSACCIONES,
            FilterExpression="cliente_id = :cid",
            ExpressionAttributeValues={":cid": {"S": cliente_id}}
        )
        items = response.get('Items', [])
        return [
            {
                'transaccion_id': item['transaccion_id']['S'],
                'cliente_id': item['cliente_id']['S'],
                'estado': item.get('estado', {}).get('S', 'desconocido'),  # 👈 evita el KeyError
                'tipo': item['tipo']['S'],
                'fondo_id': item['fondo_id']['S'],
                'fondo_nombre': item['fondo_nombre']['S'],
                'monto': int(item['monto']['N']),
                'fecha': item['fecha']['S']
            }
            for item in items
        ]
    except ClientError as e:
        raise Exception(f"❌ Error al obtener historial: {e.response['Error']['Message']}")

# ✅ Obtener fondo por ID
def obtener_transacciones_apertura(cliente_id: str, fondo_id: str):
    tabla_transacciones = dynamodb.Table('Transacciones')
    response = tabla_transacciones.scan(
        FilterExpression=Attr('cliente_id').eq(cliente_id) &
                         Attr('fondo_id').eq(fondo_id) &
                         Attr('tipo').eq('apertura')
    )
    return response.get("Items", [])

def obtener_fondo_por_id(fondo_id: str):
    try:
        tabla_fondos = dynamodb.Table(TABLE_FONDOS)
        response = tabla_fondos.get_item(Key={"FondoId": fondo_id})
        return response.get("Item")
    except ClientError as e:
        raise Exception(f"❌ Error al consultar fondo: {e.response['Error']['Message']}")

# ✅ Obtener saldo del cliente, con inicialización si no existe
def obtener_saldo_cliente(cliente_id: str) -> int:
    try:
        tabla_saldo = dynamodb.Table(TABLE_USUARIO_SALDO)
        response = tabla_saldo.get_item(Key={'cliente_id': cliente_id})
        item = response.get('Item')

        if not item:
            # Inicializar saldo en 500.000 si el cliente no existe
            saldo_inicial = 500000
            actualizar_saldo_cliente(cliente_id, saldo_inicial)
            return saldo_inicial

        return int(item['saldo'])
    except ClientError as e:
        raise Exception(f"❌ Error al obtener saldo del cliente: {e.response['Error']['Message']}")

# ✅ Actualizar saldo del cliente
def actualizar_saldo_cliente(cliente_id: str, nuevo_saldo: int):
    try:
        tabla_saldo = dynamodb.Table(TABLE_USUARIO_SALDO)
        tabla_saldo.put_item(
            Item={
                'cliente_id': cliente_id,
                'saldo': nuevo_saldo
            }
        )
    except ClientError as e:
        raise Exception(f"❌ Error al actualizar saldo: {e.response['Error']['Message']}")
