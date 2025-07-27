# 📊 API de Fondos de Inversión – FastAPI + DynamoDB

API REST para gestionar suscripciones a fondos de inversión, construida con **FastAPI** y **AWS DynamoDB**.

Incluye:
- Suscripción y cancelación de fondos.
- Consultas de historial de transacciones por cliente.
- Protección mediante API Key.
- Modularidad y estructura profesional.

---

## 📁 Estructura del proyecto

.
├── app/
│ ├── database/
│ │ └── dynamodb.py # Conexión y operaciones con DynamoDB
│ ├── dependencies/
│ │ └── auth.py # Validación de API Key
│ ├── models/
│ │ ├── schemas.py # Pydantic models (suscripciones, cancelaciones)
│ │ └── transaccion.py # Modelo de transacción
│ ├── routes/
│ │ └── fondos.py # Endpoints versionados y protegidos
│ ├── services/
│ │ ├── fondos.py # Lógica de suscripción/cancelación
│ │ └── saldo.py # Validación y actualización de saldo
│ ├── tests/
│ │ └── test_transacciones.py # Pruebas unitarias
│ ├── utils/
│ │ └── exceptions.py # Manejo de errores personalizados
├── main.py # Inicialización FastAPI
├── .env # Variables de entorno (no subir a Git)
├── README.md
└── requirements.txt


---

## 🔐 **Seguridad**

Todos los endpoints están protegidos con **API Key**.

Debes enviarla en el encabezado de la solicitud:

```http
x-api-key: TU_API_KEY


⚙️ Instalación del Proyecto
1️⃣ Clona el repositorio
git clone https://github.com/Martinfbr/cliente-fondos-app.git
cd api-fondos-inversion

2️⃣ Crea el entorno virtual
python -m venv env
source env/bin/activate      # Linux/macOS
env\\Scripts\\activate       # Windows

3️⃣ Instala dependencias
pip install -r requirements.txt

📄 Variables de entorno
Crea un archivo .env con:

AWS_ACCESS_KEY_ID=TU_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=TU_SECRET_KEY
AWS_DEFAULT_REGION=us-east-2
API_KEY=tu_api_key_secreta

▶️ Ejecutar localmente
uvicorn main:app --reload

Accede a:

Swagger: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

🚀 Endpoints disponibles (/v1/fondos)
Método	Endpoint	Descripción
POST	/suscribirse	Suscribirse a un fondo
POST	/cancelar	Cancelar fondo y devolver el monto
GET	/historial/{cliente_id}	Historial de transacciones del cliente


🗃️ Tablas DynamoDB
Tabla	Clave de partición	Propósito
Fondos	FondoId (S)	Catálogo de fondos disponibles
Transacciones	transaccion_id (S)	Registro de operaciones por cliente
UsuarioSaldo	user_id (S)	Saldo actual de cada cliente

✅ Características implementadas
Suscripción y cancelación de fondos.

Control de saldo con reembolso.

Protección con API Key.

Excepciones personalizadas.

Modularidad y arquitectura limpia.

Endpoints versionados (/v1/...).

Pruebas automatizadas.


🧩 Tecnologías utilizadas
Python 3.10+

FastAPI 0.116.1

DynamoDB + Boto3

Pydantic v2

Dotenv / Uvicorn


👨‍💻 Autor
Desarrollado por MARTIN BALBIN