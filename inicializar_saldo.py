# inicializar_saldo.py
import boto3
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

tabla = dynamodb.Table("UsuarioSaldo")

# Este script lo ejecutas UNA VEZ para dejar el saldo inicial
tabla.put_item(Item={
    "user_id": "martin",
    "saldo": 500000
})
print("✅ Saldo inicial de 'martin' configurado.")
