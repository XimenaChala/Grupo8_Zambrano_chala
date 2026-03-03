import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Esto obliga a Python a buscar el .env en la misma carpeta del script
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

db_url = os.getenv("DATABASE_URL")

print(f"--- Prueba de Conexión ---")
print(f"Buscando .env en: {env_path}")
print(f"URL detectada: {db_url}")

if not db_url:
    print("❌ Error: DATABASE_URL sigue siendo None.")
    print("Contenido de la carpeta según Python:", os.listdir(script_dir))
else:
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user;"))
            row = result.fetchone()
            print(f"✅ ¡Conexión exitosa!")
            print(f"Base de datos: {row[0]} | Usuario: {row[1]}")
    except Exception as e:
        print(f"❌ Falló la conexión: {e}")