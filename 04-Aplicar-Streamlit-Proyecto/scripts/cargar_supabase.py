"""
cargar_supabase.py - Carga el CSV a Supabase PostgreSQL
"""
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

host     = os.getenv("DB_HOST")
port     = os.getenv("DB_PORT", "6543")
dbname   = os.getenv("DB_NAME", "postgres")
user     = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
)

# Cargar CSV
csv_path = os.path.join(os.path.dirname(__file__), "../data/worldbank_pib.csv")
df = pd.read_csv(csv_path)

# Filtrar columnas que existen en la tabla
columnas_tabla = [
    "pais_codigo", "pais_nombre", "anio",
    "pib_usd", "crecimiento_pib_pct", "pib_per_capita_usd",
    "inflacion_pct", "desempleo_pct",
    "exportaciones_pct_pib", "importaciones_pct_pib",
    "region", "es_colombia", "fecha_extraccion"
]
df = df[[c for c in columnas_tabla if c in df.columns]]
df["fecha_extraccion"] = pd.to_datetime(df["fecha_extraccion"])

# Limpiar tabla antes de cargar
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE indicadores_pib RESTART IDENTITY"))
    conn.commit()
    print("🗑️  Tabla limpiada")

# Cargar datos frescos
df.to_sql(
    "indicadores_pib",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print(f"✅ {len(df)} registros cargados a Supabase")

# Verificar
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM indicadores_pib"))
    count = result.fetchone()[0]
    print(f"✅ Total en tabla: {count} registros")