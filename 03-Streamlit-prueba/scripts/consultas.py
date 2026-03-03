"""
Consultas reutilizables para los dashboards de Streamlit.
"""
import pandas as pd
from sqlalchemy import text
from scripts.database import engine


def get_clima_actual() -> pd.DataFrame:
    """Último registro de clima por ciudad."""
    query = """
        SELECT DISTINCT ON (ciudad)
            ciudad, pais, temperatura, sensacion_termica,
            humedad, velocidad_viento, descripcion, fecha_extraccion
        FROM clima
        ORDER BY ciudad, fecha_extraccion DESC;
    """
    return pd.read_sql(query, engine)


def get_clima_historico(fecha_inicio=None, fecha_fin=None) -> pd.DataFrame:
    """Todos los registros, con filtro opcional de fechas."""
    query = "SELECT * FROM clima WHERE 1=1"
    params = {}

    if fecha_inicio:
        query += " AND fecha_extraccion >= :inicio"
        params['inicio'] = fecha_inicio
    if fecha_fin:
        query += " AND fecha_extraccion <= :fin"
        params['fin'] = fecha_fin

    query += " ORDER BY fecha_extraccion DESC"
    return pd.read_sql(text(query), engine, params=params)


def get_estadisticas_ciudad(ciudad: str) -> pd.DataFrame:
    """Estadísticas agregadas para una ciudad específica."""
    query = """
        SELECT
            ciudad,
            COUNT(*)                    AS total_registros,
            ROUND(AVG(temperatura)::numeric, 1)      AS temp_promedio,
            MAX(temperatura)            AS temp_max,
            MIN(temperatura)            AS temp_min,
            ROUND(AVG(humedad)::numeric, 1)          AS humedad_promedio,
            ROUND(AVG(velocidad_viento)::numeric, 1) AS viento_promedio
        FROM clima
        WHERE ciudad = :ciudad
        GROUP BY ciudad;
    """
    return pd.read_sql(text(query), engine, params={'ciudad': ciudad})


def get_metricas_etl(limite: int = 20) -> pd.DataFrame:
    """Últimas ejecuciones del ETL."""
    query = f"""
        SELECT fecha_ejecucion, estado, registros_extraidos,
               registros_guardados, registros_fallidos,
               tiempo_ejecucion_segundos
        FROM metricas_etl
        ORDER BY fecha_ejecucion DESC
        LIMIT {limite};
    """
    return pd.read_sql(query, engine)
