import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

TABLE_SALDO = 'UsuarioSaldo'

def obtener_saldo(cliente_id: str) -> int:
    tabla = dynamodb.Table(TABLE_SALDO)
    try:
        response = tabla.get_item(Key={'user_id': cliente_id})
        if 'Item' not in response:
            raise ValueError(f"No existe saldo para el usuario {cliente_id}")
        return int(response['Item']['saldo'])
    except ClientError as e:
        raise Exception(f"Error al obtener saldo: {e.response['Error']['Message']}")

def actualizar_saldo(cliente_id: str, nuevo_saldo: int):
    tabla = dynamodb.Table(TABLE_SALDO)
    try:
        tabla.update_item(
            Key={'user_id': cliente_id},
            UpdateExpression="set saldo = :s",
            ExpressionAttributeValues={':s': Decimal(nuevo_saldo)}
        )
    except ClientError as e:
        raise Exception(f"Error al actualizar saldo: {e.response['Error']['Message']}")
