"""
consultas.py - Queries reutilizables para el dashboard
"""

import pandas as pd
from database import cargar_datos


def get_df() -> pd.DataFrame:
    df = cargar_datos()
    if not df.empty:
        df["anio"] = df["anio"].astype(int)
    return df


def colombia_vs_latam(df: pd.DataFrame = None) -> pd.DataFrame:
    df = df if df is not None else get_df()
    latam = df[df["region"] == "América Latina"].groupby("anio")["crecimiento_pib_pct"].mean().reset_index()
    latam.columns = ["anio", "latam_promedio"]
    co = df[df["pais_codigo"] == "CO"][["anio", "crecimiento_pib_pct"]].rename(
        columns={"crecimiento_pib_pct": "colombia"}
    )
    return pd.merge(co, latam, on="anio").dropna()


def ranking_pib_pc(df: pd.DataFrame, anio: int) -> pd.DataFrame:
    sub = df[(df["anio"] == anio)].dropna(subset=["pib_per_capita_usd"])
    sub = sub[["pais_nombre", "pais_codigo", "pib_per_capita_usd"]].sort_values(
        "pib_per_capita_usd", ascending=False
    ).reset_index(drop=True)
    sub.index += 1
    return sub


def evolucion_pib(df: pd.DataFrame, paises: list) -> pd.DataFrame:
    return df[df["pais_codigo"].isin(paises)].dropna(subset=["pib_usd"])[
        ["pais_nombre", "anio", "pib_usd"]
    ].sort_values(["pais_nombre", "anio"])


def colombia_detalle(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["pais_codigo"] == "CO"].sort_values("anio").reset_index(drop=True)


def balanza_comercial(df: pd.DataFrame) -> pd.DataFrame:
    sub = df.dropna(subset=["exportaciones_pct_pib", "importaciones_pct_pib"]).copy()
    sub["balanza"] = sub["exportaciones_pct_pib"] - sub["importaciones_pct_pib"]
    return sub[["pais_nombre", "pais_codigo", "anio", "balanza"]].sort_values(["pais_codigo", "anio"])
"""
consultas.py - Lógica de procesamiento de datos con Pandas para el Dashboard
"""
import pandas as pd

def colombia_detalle(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra y devuelve solo los datos de Colombia ordenados por año."""
    return df[df["pais_codigo"] == "CO"].sort_values("anio").copy()

def colombia_vs_latam(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el promedio de crecimiento de LATAM y lo compara con Colombia."""
    # Promedio de la región (excluyendo Colombia si lo deseas, o incluyéndola)
    latam = df[df["es_colombia"] == False].groupby("anio")["crecimiento_pib_pct"].mean().reset_index()
    latam.rename(columns={"crecimiento_pib_pct": "latam_promedio"}, inplace=True)
    
    co = df[df["pais_codigo"] == "CO"][["anio", "crecimiento_pib_pct"]]
    co.rename(columns={"crecimiento_pib_pct": "colombia"}, inplace=True)
    
    comp = pd.merge(latam, co, on="anio", how="inner")
    return comp

def ranking_pib_pc(df: pd.DataFrame, anio_rank: int) -> pd.DataFrame:
    """Retorna el Top 10 de países por PIB per cápita para un año específico."""
    filtro_anio = df[df["anio"] == anio_rank].dropna(subset=["pib_per_capita_usd"])
    rank = filtro_anio.sort_values("pib_per_capita_usd", ascending=False).head(10)
    # Ordenamos ascendente para que en la gráfica horizontal el mayor quede arriba
    return rank.sort_values("pib_per_capita_usd", ascending=True).copy()

def balanza_comercial(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la diferencia entre exportaciones e importaciones."""
    bal = df.dropna(subset=["exportaciones_pct_pib", "importaciones_pct_pib"]).copy()
    bal["balanza"] = bal["exportaciones_pct_pib"] - bal["importaciones_pct_pib"]
    return bal.sort_values("anio")