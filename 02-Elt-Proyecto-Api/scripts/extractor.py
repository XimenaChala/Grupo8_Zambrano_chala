#!/usr/bin/env python3
"""
ETL Extractor - World Bank API
Extrae indicadores de PIB y crecimiento económico para Colombia y países comparados.
API: https://api.worldbank.org/v2/
No requiere API key - es pública y gratuita.
"""

import os
import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ─── Indicadores del World Bank que vamos a extraer ─────────────────────────
INDICADORES = {
    "NY.GDP.MKTP.CD":     "pib_usd",              # PIB en USD corrientes
    "NY.GDP.MKTP.KD.ZG":  "crecimiento_pib_pct",  # Crecimiento del PIB (%)
    "NY.GDP.PCAP.CD":     "pib_per_capita_usd",    # PIB per cápita USD
    "NY.GDP.PCAP.KD.ZG":  "crecimiento_pib_pc_pct",# Crecimiento PIB per cápita (%)
    "FP.CPI.TOTL.ZG":     "inflacion_pct",         # Inflación (%)
    "SL.UEM.TOTL.ZS":     "desempleo_pct",         # Desempleo (% fuerza laboral)
    "NE.EXP.GNFS.ZS":     "exportaciones_pct_pib", # Exportaciones % del PIB
    "NE.IMP.GNFS.ZS":     "importaciones_pct_pib", # Importaciones % del PIB
}


class WorldBankExtractor:
    """Extrae datos económicos del World Bank API v2."""

    BASE_URL = "https://api.worldbank.org/v2"

    def __init__(self):
        self.paises   = os.getenv("COUNTRIES", "CO,US,BR,MX,AR,CL,PE").split(",")
        self.start_yr = os.getenv("START_YEAR", "2000")
        self.end_yr   = os.getenv("END_YEAR",   "2023")
        logger.info(f"Extractor iniciado | Países: {self.paises} | Años: {self.start_yr}-{self.end_yr}")

    # ── Llamada a la API ──────────────────────────────────────────────────────
    def _get_indicador(self, pais: str, indicador: str) -> list:
        """Llama al endpoint del World Bank y retorna lista de registros."""
        url = (
            f"{self.BASE_URL}/country/{pais}/indicator/{indicador}"
            f"?format=json&date={self.start_yr}:{self.end_yr}&per_page=100"
        )
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            # La respuesta viene como [metadata, [registros]]
            if len(data) < 2 or not isinstance(data[1], list):
                logger.warning(f"Sin datos: {pais} / {indicador}")
                return []

            return data[1]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error HTTP para {pais}/{indicador}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado para {pais}/{indicador}: {e}")
            return []

    # ── Procesar registros crudos ─────────────────────────────────────────────
    def _procesar_registros(self, registros: list, nombre_col: str) -> list:
        """Convierte registros raw del API a dicts limpios."""
        filas = []
        for r in registros:
            if r.get("value") is None:
                continue  # saltar años sin dato
            filas.append({
                "pais_codigo": r["country"]["id"],
                "pais_nombre": r["country"]["value"],
                "anio":        int(r["date"]),
                nombre_col:    r["value"],
            })
        return filas

    # ── Extracción completa ───────────────────────────────────────────────────
    def ejecutar_extraccion(self) -> pd.DataFrame:
        """
        Extrae todos los indicadores para todos los países y
        devuelve un DataFrame combinado.
        """
        todos_df = []

        for pais in self.paises:
            pais = pais.strip().upper()
            logger.info(f"── Procesando país: {pais}")
            df_pais = None

            for codigo_ind, nombre_col in INDICADORES.items():
                registros = self._get_indicador(pais, codigo_ind)
                filas = self._procesar_registros(registros, nombre_col)

                if not filas:
                    continue

                df_ind = pd.DataFrame(filas)

                if df_pais is None:
                    df_pais = df_ind
                else:
                    # Merge por país + año para ir agregando columnas
                    df_pais = pd.merge(
                        df_pais, df_ind,
                        on=["pais_codigo", "pais_nombre", "anio"],
                        how="outer"
                    )
                logger.info(f"  ✅ {nombre_col}: {len(filas)} registros")

            if df_pais is not None:
                todos_df.append(df_pais)

        if not todos_df:
            logger.error("No se extrajeron datos.")
            return pd.DataFrame()

        df_final = pd.concat(todos_df, ignore_index=True)
        df_final["fecha_extraccion"] = datetime.now().isoformat()
        df_final = df_final.sort_values(["pais_codigo", "anio"]).reset_index(drop=True)

        logger.info(f"Extracción completa: {len(df_final)} filas | {df_final['pais_codigo'].nunique()} países")
        return df_final


# ── TRANSFORMACIÓN ────────────────────────────────────────────────────────────
class WorldBankTransformer:
    """Limpia y enriquece el DataFrame extraído."""

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df = df.copy()

        # Redondear decimales
        cols_num = df.select_dtypes(include="number").columns.tolist()
        df[cols_num] = df[cols_num].round(4)

        # Columna de región (simplificada)
        latinoamerica = {"CO", "BR", "MX", "AR", "CL", "PE"}
        df["region"] = df["pais_codigo"].apply(
            lambda c: "América Latina" if c in latinoamerica else "Referencia"
        )

        # Marcar si es Colombia (país foco del análisis)
        df["es_colombia"] = df["pais_codigo"] == "CO"

        logger.info("Transformación completada.")
        return df


# ── CARGA ─────────────────────────────────────────────────────────────────────
class WorldBankLoader:
    """Guarda los datos transformados en CSV, JSON y (opcional) PostgreSQL."""

    def __init__(self):
        os.makedirs("data", exist_ok=True)

    def guardar_csv(self, df: pd.DataFrame):
        path = "data/worldbank_pib.csv"
        df.to_csv(path, index=False, encoding="utf-8")
        logger.info(f"📁 CSV guardado: {path}")

    def guardar_json(self, df: pd.DataFrame):
        path = "data/worldbank_pib_raw.json"
        df.to_json(path, orient="records", indent=2, force_ascii=False)
        logger.info(f"📁 JSON guardado: {path}")

    def guardar_postgresql(self, df: pd.DataFrame):
        """Carga a PostgreSQL si están configuradas las variables de entorno."""
        try:
            from sqlalchemy import create_engine, text

            host   = os.getenv("DB_HOST", "localhost")
            port   = os.getenv("DB_PORT", "5432")
            dbname = os.getenv("DB_NAME", "worldbank_db")
            user   = os.getenv("DB_USER", "postgres")
            pw     = os.getenv("DB_PASSWORD", "")

            engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{dbname}")

            # Crear tabla si no existe
            with engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS indicadores_pib (
                        id                      SERIAL PRIMARY KEY,
                        pais_codigo             VARCHAR(3),
                        pais_nombre             VARCHAR(100),
                        anio                    INTEGER,
                        pib_usd                 NUMERIC(20,4),
                        crecimiento_pib_pct     NUMERIC(10,4),
                        pib_per_capita_usd      NUMERIC(15,4),
                        crecimiento_pib_pc_pct  NUMERIC(10,4),
                        inflacion_pct           NUMERIC(10,4),
                        desempleo_pct           NUMERIC(10,4),
                        exportaciones_pct_pib   NUMERIC(10,4),
                        importaciones_pct_pib   NUMERIC(10,4),
                        region                  VARCHAR(50),
                        es_colombia             BOOLEAN,
                        fecha_extraccion        TIMESTAMP,
                        UNIQUE (pais_codigo, anio)
                    );
                """))
                conn.commit()

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

        except ImportError:
            logger.warning("sqlalchemy/psycopg2 no instalados. Omitiendo carga a PostgreSQL.")
        except Exception as e:
            logger.error(f"Error cargando a PostgreSQL: {e}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  ETL - World Bank API | PIB y Crecimiento Económico")
    print("="*60)

    # 1. EXTRACT
    extractor = WorldBankExtractor()
    df_raw = extractor.ejecutar_extraccion()

    if df_raw.empty:
        logger.error("Extracción vacía. Verifica tu conexión a internet.")
        exit(1)

    # 2. TRANSFORM
    transformer = WorldBankTransformer()
    df_clean = transformer.transformar(df_raw)

    # 3. LOAD
    loader = WorldBankLoader()
    loader.guardar_csv(df_clean)
    loader.guardar_json(df_clean)
    loader.guardar_postgresql(df_clean)

    # Resumen en consola
    print("\n" + "="*60)
    print("RESUMEN DE EXTRACCIÓN")
    print("="*60)
    print(f"Registros totales : {len(df_clean)}")
    print(f"Países            : {df_clean['pais_nombre'].unique().tolist()}")
    print(f"Años              : {df_clean['anio'].min()} - {df_clean['anio'].max()}")
    print(f"Columnas          : {list(df_clean.columns)}")
    print("="*60)
    print("\nPrimeras filas:")
    print(df_clean.head(10).to_string())
    print("="*60)
    print("\n✅ ETL completado exitosamente.")
