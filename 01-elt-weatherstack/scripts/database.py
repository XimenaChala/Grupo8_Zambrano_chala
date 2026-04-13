import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar variables del archivo .env
load_dotenv()

# Obtener la URL desde el .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no está definida en el archivo .env")

# Crear el engine de conexión
engine = create_engine(DATABASE_URL)
