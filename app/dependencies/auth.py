from fastapi import Header, HTTPException, status
from dotenv import load_dotenv
import os

# 👉 Cargar variables de entorno desde .env
load_dotenv()

# 👉 Leer API Key desde las variables de entorno
API_KEY = os.getenv("API_KEY")

# 👉 Verificador de la API Key
def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ No autorizado: API key inválida",
        )
