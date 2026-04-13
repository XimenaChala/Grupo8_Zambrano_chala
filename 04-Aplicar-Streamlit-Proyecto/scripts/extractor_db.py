"""
extractor_db.py - Extrae del World Bank API y carga directo a PostgreSQL
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from extractor import ejecutar
from database import get_engine, test_conexion
from models import crear_tablas
import logging

logger = logging.getLogger(__name__)


def cargar_a_postgres(df):
    if not test_conexion():
        logger.error("❌ No hay conexión a PostgreSQL. Verifica tu .env")
        return False

    engine = get_engine()
    crear_tablas(engine)

    import pandas as pd
    df_pg = df.copy()
    df_pg["fecha_extraccion"] = pd.to_datetime(df_pg["fecha_extraccion"])

    df_pg.to_sql(
        "indicadores_pib",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )
    logger.info(f"🐘 PostgreSQL: {len(df_pg)} filas cargadas en 'indicadores_pib'")
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    print("Extrayendo datos de la API...")
    df = ejecutar()

    if df is not None:
        print("Cargando a PostgreSQL...")
        exito = cargar_a_postgres(df)
        if exito:
            print("✅ Datos cargados a PostgreSQL exitosamente.")
        else:
            print("⚠️  Datos guardados solo en CSV.")
