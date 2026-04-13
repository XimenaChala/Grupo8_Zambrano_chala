"""
database.py - Conexión a PostgreSQL (local o nube)
Maneja la conexión con fallback a CSV si no hay BD disponible.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import logging

load_dotenv()
logger = logging.getLogger(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/worldbank_pib.csv")
CSV_FALLBACK = os.path.join(os.path.dirname(__file__), "../../02-Elt-Proyecto-Api/data/worldbank_pib.csv")


def get_engine():
    host   = os.getenv("DB_HOST", "localhost")
    port   = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "worldbank_db")
    user   = os.getenv("DB_USER", "postgres")
    pw     = os.getenv("DB_PASSWORD", "")
    url    = f"postgresql://{user}:{pw}@{host}:{port}/{dbname}"
    return create_engine(url)


def test_conexion() -> bool:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def cargar_datos() -> pd.DataFrame:
    if test_conexion():
        try:
            engine = get_engine()
            df = pd.read_sql("SELECT * FROM indicadores_pib ORDER BY pais_codigo, anio", engine)
            logger.info(f"✅ Datos cargados desde PostgreSQL: {len(df)} filas")
            return df
        except Exception as e:
            logger.warning(f"Error leyendo PostgreSQL: {e}. Usando CSV.")

    for ruta in [CSV_PATH, CSV_FALLBACK]:
        if os.path.exists(ruta):
            df = pd.read_csv(ruta)
            logger.info(f"📁 Datos cargados desde CSV: {ruta}")
            return df

    logger.error("No se encontró fuente de datos.")
    return pd.DataFrame()
