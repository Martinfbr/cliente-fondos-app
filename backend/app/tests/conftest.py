import pytest
from moto import mock_aws
import boto3
import os

@pytest.fixture(scope="function")
def aws_setup():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
        sns = boto3.client("sns", region_name="us-east-2")

        # Agregar variable SNS_TOPIC_ARN para las pruebas
        os.environ["SNS_TOPIC_ARN"] = "arn:aws:sns:us-east-2:123456789012:TestTopic"

        # Crear tablas
        dynamodb.create_table(
            TableName="Fondos",
            KeySchema=[{"AttributeName": "FondoId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "FondoId", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        dynamodb.create_table(
            TableName="UsuarioSaldo",
            KeySchema=[{"AttributeName": "user_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "user_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        dynamodb.create_table(
            TableName="Transacciones",
            KeySchema=[{"AttributeName": "transaccion_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "transaccion_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        yield dynamodb, sns
