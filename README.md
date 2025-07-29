# 📊 **API de Fondos de Inversión – FastAPI + DynamoDB**

Este proyecto implementa un sistema de gestión de fondos (suscripción, historial y cancelación). Incluye:

Backend en FastAPI.

Frontend en React.

Infraestructura desplegable en AWS mediante CloudFormation.


## ✅ **Características implementadas**

- Gestión de Fondos: Permite suscribirse a fondos, consultar historial y cancelar suscripciones.
- Backend con FastAPI: Arquitectura modular con manejo de excepciones personalizadas y pruebas unitarias.
- Integración con AWS DynamoDB: Persistencia de datos para usuarios, fondos y transacciones.
- Notificaciones vía SNS: Envío de notificaciones al suscribirse o cancelar fondos.
- Frontend en React: Interfaz sencilla para gestionar fondos y visualizar historial.
- Despliegue automatizado con CloudFormation: Plantillas para backend (API Gateway + Lambda + DynamoDB) y frontend (S3 + CloudFront).
- Variables de entorno parametrizables: Manejo de configuraciones para entornos de desarrollo y producción.
- Pruebas automatizadas con Pytest: Validación de la lógica de negocio y de las integraciones con AWS.
- Estructura clara del proyecto: Separación entre backend, frontend e infraestructura.
- Documentación de despliegue: Pasos detallados para ejecutar y desplegar en AWS.

---

## 📁 **Estructura del Proyecto**

```
Backend/
    ├── app/
    │   ├── models/
    │   │   └── transacciones_models.py      # Modelo de transacción
    │   ├── routes/
    │   │   └── fondos.py           # Endpoints versionados y protegidos
    │   │   └── transacciones.py    # Endpoints versionados y protegidos
    │   ├── services/
    │   │   ├── dynamodb_service          # Lógica de suscripción/cancelación
    │   ├── tests/
    │   │   └── test_routes_transacciones.py  # Pruebas unitarias
    │   │   └── conftest.py  # Pruebas unitarias
    │   │   └── test_services.py  # Pruebas unitarias
    │   ├── utils/
    │   │   └── exceptions.py       # Manejo de errores personalizados
    ├── main.py                     # Inicialización FastAPI
    ├── README.md
    └── requirements.txt
    └── handler.py
frontend/
    ├── src/
    │   ├── components/
    │   │   └── Fondos.jsx      # front fondos
    │   │   └── Historial.jsx   # front historial
    ├── app.js
    ├── index.js
    ├── .env
cloudformation/
    ├── .aws-sam/
    ├── frontend-s3-cloudfront.yaml  # Infraestructura frontend (S3 + CloudFront)
    ├── samconfig.toml 
    ├── template.yaml # Infraestructura backend (API Gateway + DynamoDB + Lambda)
README.md

```

---


## ⚙️ **Instalación del Proyecto**

### 1️⃣ Clona el repositorio

```bash
git clone https://github.com/Martinfbr/cliente-fondos-app.git
cd api-fondos-inversion
```

### 2️⃣ Instalación – Backend

```bash

Clonar repositorio:

cd proyecto-app/backend

Crear y activar entorno virtual:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Instalar dependencias:

pip install -r requirements.txt

Ejecutar servidor local:

uvicorn main:app --reload

```
### 3️⃣ Instalación – Frontend

```bash

Ir al directorio frontend:

cd proyecto-app/frontend

Instalar dependencias:

npm install

Ejecutar en local:
```

Accede a:
- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

Rutas en Produccion
-PROD: https://9feflclol0.execute-api.us-east-2.amazonaws.com/Prod/docs
-REACT: https://dpiww6892pqew.cloudfront.net/
---

## 🚀 **Endpoints disponibles** (https://9feflclol0.execute-api.us-east-2.amazonaws.com/Prod/docs)

| Método | Endpoint                      | Descripción                          |
|--------|-------------------------------|--------------------------------------|
| POST   | `/suscribirse`                | Suscribirse a un fondo               |
| POST   | `/cancelar`                   | Cancelar fondo y devolver el monto   |
| GET    | `/historial/{cliente_id}`     | Historial de transacciones del cliente |

---

## 🗃️ **Tablas DynamoDB**

| Tabla           | Clave de partición     | Propósito                                     |
|------------------|-------------------------|-----------------------------------------------|
| `Fondos`         | `FondoId (S)`           | Catálogo de fondos disponibles                |
| `Transacciones`  | `transaccion_id (S)`    | Registro de operaciones por cliente           |
| `UsuarioSaldo`   | `user_id (S)`           | Saldo actual de cada cliente                  |

---


## 🧩 **Despliegue con CloudFormation**

Despliegue con CloudFormation

Este proyecto incluye plantillas YAML para desplegar frontend y backend en AWS.

1. Despliegue del Backend

Plantilla: cloudformation/template.yaml

Crear stack:

aws cloudformation create-stack \
  --stack-name backendfondospruebatecnica \
  --template-body file://C:/Personal/proyecto-app/cloudformation/template.yaml \
  --capabilities CAPABILITY_IAM

Actualizar stack:

aws cloudformation update-stack \
  --stack-name backendfondospruebatecnica \
  --template-body file://C:/Personal/proyecto-app/cloudformation/template.yaml \
  --capabilities CAPABILITY_IAM

Eliminar stack:

aws cloudformation delete-stack --stack-name backendfondospruebatecnica

2. Despliegue del Frontend

Plantilla: cloudformation/frontend-s3-cloudfront.yaml

Crear stack:

aws cloudformation create-stack \
  --stack-name frontendfondospruebatecnica \
  --template-body file://C:/Personal/proyecto-app/cloudformation/frontend-s3-cloudfront.yaml \
  --parameters ParameterKey=BucketName,ParameterValue=frontendfondospruebatecnica \
  --capabilities CAPABILITY_IAM

Actualizar stack:

aws cloudformation update-stack \
  --stack-name frontendfondospruebatecnica \
  --template-body file://C:/Personal/proyecto-app/cloudformation/frontend-s3-cloudfront.yaml \
  --parameters ParameterKey=BucketName,ParameterValue=frontendfondospruebatecnica \
  --capabilities CAPABILITY_IAM

Eliminar stack:

aws cloudformation delete-stack --stack-name frontendfondospruebatecnica

3. Subir archivos del Frontend a S3

Compilar y subir a bucket S3:

cd frontend
npm run build
aws s3 sync build/ s3://frontendfondospruebatecnica

4. Conectar Frontend con Backend

Obtener URL del API Gateway del backend:

aws cloudformation describe-stacks \
  --stack-name backendfondospruebatecnica \
  --query "Stacks[0].Outputs"

Configurar la URL en .env.production del frontend:

VITE_API_URL=https://<API_GATEWAY_URL>

Reconstruir y volver a subir a S3:

---

## 👨‍💻 Autor

Desarrollado por **MARTIN BALBIN**.