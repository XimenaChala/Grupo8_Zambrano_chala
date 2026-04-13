#!/usr/bin/env python3
"""
transformador.py - Transformación de datos World Bank
Limpia, enriquece y valida el DataFrame extraído por extractor.py
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class WorldBankTransformer:

    LATAM = {"CO", "BR", "MX", "AR", "CL", "PE"}

    def limpiar_nulos(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_num = [
            "pib_usd", "crecimiento_pib_pct", "pib_per_capita_usd",
            "crecimiento_pib_pc_pct", "inflacion_pct", "desempleo_pct",
            "exportaciones_pct_pib", "importaciones_pct_pib",
        ]
        cols_existentes = [c for c in cols_num if c in df.columns]
        antes = len(df)
        df = df.dropna(subset=cols_existentes, how="all")
        logger.info(f"Limpieza nulos: {antes - len(df)} filas eliminadas")
        return df.reset_index(drop=True)

    def redondear_decimales(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_num = df.select_dtypes(include="number").columns.tolist()
        df[cols_num] = df[cols_num].round(4)
        return df

    def agregar_region(self, df: pd.DataFrame) -> pd.DataFrame:
        df["region"] = df["pais_codigo"].apply(
            lambda c: "América Latina" if c in self.LATAM else "Referencia"
        )
        return df

    def agregar_flag_colombia(self, df: pd.DataFrame) -> pd.DataFrame:
        df["es_colombia"] = df["pais_codigo"] == "CO"
        return df

    def agregar_balanza_comercial(self, df: pd.DataFrame) -> pd.DataFrame:
        if "exportaciones_pct_pib" in df.columns and "importaciones_pct_pib" in df.columns:
            df["balanza_comercial_pct"] = (
                df["exportaciones_pct_pib"] - df["importaciones_pct_pib"]
            ).round(4)
        return df

    def validar_tipos(self, df: pd.DataFrame) -> pd.DataFrame:
        df["anio"]        = df["anio"].astype(int)
        df["pais_codigo"] = df["pais_codigo"].astype(str).str.upper().str.strip()
        df["pais_nombre"] = df["pais_nombre"].astype(str).str.strip()
        return df

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            logger.warning("DataFrame vacío, no hay nada que transformar.")
            return df

        logger.info("Iniciando transformaciones...")
        df = self.validar_tipos(df)
        df = self.limpiar_nulos(df)
        df = self.redondear_decimales(df)
        df = self.agregar_region(df)
        df = self.agregar_flag_colombia(df)
        df = self.agregar_balanza_comercial(df)

        logger.info(f"Transformación completa: {len(df)} filas | {len(df.columns)} columnas")
        return df


if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    ruta_csv = "data/worldbank_pib.csv"
    if not os.path.exists(ruta_csv):
        print(f"❌ No se encontró {ruta_csv}. Ejecuta primero extractor.py")
        exit(1)

    df_raw = pd.read_csv(ruta_csv)
    print(f"Filas antes de transformar: {len(df_raw)}")

    transformer = WorldBankTransformer()
    df_clean = transformer.transformar(df_raw)

    df_clean.to_csv(ruta_csv, index=False)
    print(f"✅ Datos transformados guardados en {ruta_csv}")
    print(df_clean.head())
