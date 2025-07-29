from app.services.dynamodb_service import suscribir_a_fondo, obtener_historial
import boto3
import os

def test_suscribir_exitoso(aws_setup):
    dynamodb, _ = aws_setup

    # Setear variable SNS_TOPIC_ARN
    os.environ["SNS_TOPIC_ARN"] = "arn:aws:sns:us-east-2:123456789012:TestTopic"

    # Poblar tablas
    fondos = dynamodb.Table("Fondos")
    usuario_saldo = dynamodb.Table("UsuarioSaldo")

    fondos.put_item(Item={"FondoId": "1", "Nombre": "Fondo Test", "MontoMinimo": 1000})
    usuario_saldo.put_item(Item={"user_id": "123", "saldo": 5000, "metodo_notificacion": "email", "contacto": "user@test.com"})

    # Ejecutar suscripción
    result = suscribir_a_fondo("123", "1", 2000)

    assert result["status"] == "success"
    assert "transaccion_id" in result
