import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Carga variables del entorno
load_dotenv()

try:
    # Conexión a DynamoDB
    dynamodb = boto3.client(
        'dynamodb',
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    # Listar tablas
    response = dynamodb.list_tables()
    print("✅ Conexión exitosa. Tablas encontradas en DynamoDB:")
    for nombre in response.get("TableNames", []):
        print(f" - {nombre}")

except ClientError as e:
    print(f"❌ Error al conectar con DynamoDB: {e.response['Error']['Message']}")
except Exception as e:
    print(f"⚠️ Otro error: {e}")
