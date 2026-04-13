"""
extractor.py - Extrae datos del World Bank API y guarda en CSV
"""

import os
import requests
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INDICADORES = {
    "NY.GDP.MKTP.CD":    "pib_usd",
    "NY.GDP.MKTP.KD.ZG": "crecimiento_pib_pct",
    "NY.GDP.PCAP.CD":    "pib_per_capita_usd",
    "FP.CPI.TOTL.ZG":    "inflacion_pct",
    "SL.UEM.TOTL.ZS":    "desempleo_pct",
    "NE.EXP.GNFS.ZS":    "exportaciones_pct_pib",
    "NE.IMP.GNFS.ZS":    "importaciones_pct_pib",
}

PAISES     = ["CO", "US", "BR", "MX", "AR", "CL", "PE"]
START_YEAR = "2000"
END_YEAR   = "2023"
BASE_URL   = "https://api.worldbank.org/v2"


def extraer_indicador(pais, indicador, nombre_col):
    url = f"{BASE_URL}/country/{pais}/indicator/{indicador}?format=json&date={START_YEAR}:{END_YEAR}&per_page=100"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if len(data) < 2:
            return []
        filas = []
        for r in data[1]:
            if r.get("value") is None:
                continue
            filas.append({
                "pais_codigo": r["country"]["id"],
                "pais_nombre": r["country"]["value"],
                "anio":        int(r["date"]),
                nombre_col:    r["value"],
            })
        return filas
    except Exception as e:
        logger.error(f"Error {pais}/{indicador}: {e}")
        return []


def ejecutar():
    os.makedirs("data", exist_ok=True)
    todos = []

    for pais in PAISES:
        df_pais = None
        for codigo, nombre_col in INDICADORES.items():
            filas = extraer_indicador(pais, codigo, nombre_col)
            if not filas:
                continue
            df_ind = pd.DataFrame(filas)
            df_pais = df_ind if df_pais is None else pd.merge(
                df_pais, df_ind, on=["pais_codigo", "pais_nombre", "anio"], how="outer"
            )
            logger.info(f"✅ {pais} / {nombre_col}: {len(filas)} registros")

        if df_pais is not None:
            todos.append(df_pais)

    if not todos:
        logger.error("Sin datos extraídos.")
        return

    df = pd.concat(todos, ignore_index=True)
    df["fecha_extraccion"] = datetime.now().isoformat()
    df["region"]      = df["pais_codigo"].apply(lambda c: "América Latina" if c != "US" else "Referencia")
    df["es_colombia"] = df["pais_codigo"] == "CO"
    df = df.sort_values(["pais_codigo", "anio"]).reset_index(drop=True)

    df.to_csv("data/worldbank_pib.csv", index=False)
    logger.info(f"📁 CSV guardado: data/worldbank_pib.csv ({len(df)} filas)")
    return df


if __name__ == "__main__":
    ejecutar()
