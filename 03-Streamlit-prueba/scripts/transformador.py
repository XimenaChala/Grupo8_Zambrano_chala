#!/usr/bin/env python3
"""
transformador.py — Limpia, valida y categoriza los datos de clima.
Lee data/clima_raw.json → escribe data/clima.csv (versión limpia)
Uso: python scripts/transformador.py
"""
import os
import json
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def cargar_datos(path: str = "data/clima_raw.json") -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ No se encontró: {path}. Ejecuta demo_data.py primero.")
    with open(path, encoding="utf-8") as f:
        datos = json.load(f)
    df = pd.DataFrame(datos)
    logger.info(f"📂 Cargados {len(df)} registros desde {path}")
    return df


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    filas_antes = len(df)

    # 1. Eliminar duplicados exactos
    df = df.drop_duplicates()

    # 2. Eliminar filas con nulos en columnas críticas
    cols_criticas = ["ciudad", "temperatura", "humedad", "velocidad_viento", "fecha_extraccion"]
    df = df.dropna(subset=cols_criticas)

    # 3. Normalizar texto
    df["ciudad"]      = df["ciudad"].str.strip().str.title()
    df["pais"]        = df["pais"].str.strip().str.title()
    df["descripcion"] = df["descripcion"].str.strip().str.title()

    # 4. Convertir tipos
    df["temperatura"]       = pd.to_numeric(df["temperatura"],       errors="coerce")
    df["sensacion_termica"] = pd.to_numeric(df["sensacion_termica"], errors="coerce")
    df["humedad"]           = pd.to_numeric(df["humedad"],           errors="coerce").astype("Int64")
    df["velocidad_viento"]  = pd.to_numeric(df["velocidad_viento"],  errors="coerce")
    df["latitud"]           = pd.to_numeric(df["latitud"],           errors="coerce")
    df["longitud"]          = pd.to_numeric(df["longitud"],          errors="coerce")
    df["fecha_extraccion"]  = pd.to_datetime(df["fecha_extraccion"], errors="coerce")

    # 5. Eliminar filas donde la conversión falló
    df = df.dropna(subset=["temperatura", "humedad", "velocidad_viento", "fecha_extraccion"])

    # 6. Filtros de rango lógico
    df = df[df["temperatura"].between(-10, 50)]
    df = df[df["humedad"].between(0, 100)]
    df = df[df["velocidad_viento"].between(0, 200)]

    filas_despues = len(df)
    eliminadas = filas_antes - filas_despues
    if eliminadas:
        logger.warning(f"⚠️  {eliminadas} filas eliminadas en limpieza")
    else:
        logger.info("✅ Sin filas problemáticas — datos limpios")

    return df.reset_index(drop=True)


def categorizar(df: pd.DataFrame) -> pd.DataFrame:
    # Categoría de temperatura
    df["categoria_temp"] = pd.cut(
        df["temperatura"],
        bins=[-10, 10, 18, 24, 30, 50],
        labels=["Muy fría", "Fría", "Templada", "Cálida", "Muy cálida"]
    )

    # Categoría de humedad
    df["categoria_humedad"] = pd.cut(
        df["humedad"],
        bins=[0, 40, 60, 80, 100],
        labels=["Seca", "Moderada", "Húmeda", "Muy húmeda"]
    )

    # Índice de confort (0-100, mayor = más confortable)
    # Penaliza temperaturas extremas y humedad alta
    df["indice_confort"] = (
        100
        - abs(df["temperatura"] - 22) * 2          # ideal ~22°C
        - (df["humedad"] - 60).clip(lower=0) * 0.5  # penaliza > 60%
        - df["velocidad_viento"] * 0.3               # penaliza viento
    ).clip(0, 100).round(1)

    logger.info("✅ Columnas de categorización agregadas")
    return df


def guardar(df: pd.DataFrame, path: str = "data/clima.csv") -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    # Convertir fecha a string para el CSV
    df_out = df.copy()
    df_out["fecha_extraccion"] = df_out["fecha_extraccion"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df_out.to_csv(path, index=False)
    logger.info(f"📁 Datos transformados guardados en {path}")


def main():
    df = cargar_datos()

    print("\n📊 ANTES DE TRANSFORMAR:")
    print(df[["ciudad", "temperatura", "humedad", "velocidad_viento"]].describe().round(2))

    df = limpiar(df)
    df = categorizar(df)

    print("\n📊 DESPUÉS DE TRANSFORMAR:")
    print(df[["ciudad", "temperatura", "humedad", "categoria_temp", "indice_confort"]].head(10))

    guardar(df)

    print(f"\n✅ Transformación completa — {len(df)} registros listos para carga")


if __name__ == "__main__":
    main()