"""
database.py - Conexión a Supabase: .env local / secrets.toml en nube
"""
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/worldbank_pib.csv")


def get_engine():
    try:
        import streamlit as st
        cfg = st.secrets["database"]
        host     = cfg["host"]
        port     = cfg["port"]
        dbname   = cfg["name"]
        user     = cfg["user"]
        password = cfg["password"]
    except Exception:
        host     = os.getenv("DB_HOST")
        port     = os.getenv("DB_PORT", "6543")
        dbname   = os.getenv("DB_NAME", "postgres")
        user     = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")


def test_conexion() -> bool:
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def cargar_datos() -> pd.DataFrame:
    if test_conexion():
        try:
            df = pd.read_sql(
                "SELECT * FROM indicadores_pib ORDER BY pais_codigo, anio",
                get_engine()
            )
            logger.info(f"✅ Datos desde Supabase: {len(df)} filas")
            return df
        except Exception as e:
            logger.warning(f"Error Supabase: {e}. Usando CSV.")
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        logger.info(f"📁 Datos desde CSV: {len(df)} filas")
        return df
    return pd.DataFrame()