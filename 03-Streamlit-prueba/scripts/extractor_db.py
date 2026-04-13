#!/usr/bin/env python3
"""
extractor_db.py — Carga datos de clima en PostgreSQL/Supabase.
Lee data/clima.csv (ya transformado) y hace bulk insert.
Uso: python scripts/extractor_db.py
"""
import os
import sys
import time
import logging
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.database import SessionLocal, engine
from scripts.models import Base, Ciudad, RegistroClima, MetricasETL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/etl.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def crear_tablas():
    """Crea las tablas si no existen (útil para primera ejecución local)."""
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas verificadas/creadas")


def obtener_o_crear_ciudad(db, nombre: str, pais: str, lat: float, lon: float) -> Ciudad:
    """Retorna la ciudad existente o la crea si no existe."""
    ciudad = db.query(Ciudad).filter_by(nombre=nombre).first()
    if not ciudad:
        ciudad = Ciudad(nombre=nombre, pais=pais, latitud=lat, longitud=lon)
        db.add(ciudad)
        db.flush()  # obtiene el id sin hacer commit
        logger.info(f"🏙️  Ciudad registrada: {nombre}")
    return ciudad


def cargar_datos(csv_path: str = "data/clima.csv") -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ No se encontró {csv_path}. Ejecuta demo_data.py y transformador.py primero.")
    df = pd.read_csv(csv_path)
    df["fecha_extraccion"] = pd.to_datetime(df["fecha_extraccion"], errors="coerce")
    logger.info(f"📊 {len(df)} registros a procesar")
    return df


def bulk_insert(df: pd.DataFrame) -> tuple[int, int]:
    """Inserta todos los registros en la BD. Retorna (guardados, fallidos)."""
    db = SessionLocal()
    guardados = fallidos = 0

    try:
        # Mapa ciudad_nombre → objeto Ciudad (para evitar queries repetidas)
        ciudades_cache: dict[str, Ciudad] = {}

        for _, row in df.iterrows():
            try:
                nombre = str(row["ciudad"]).strip()

                if nombre not in ciudades_cache:
                    ciudades_cache[nombre] = obtener_o_crear_ciudad(
                        db,
                        nombre=nombre,
                        pais=str(row.get("pais", "Colombia")),
                        lat=float(row.get("latitud", 0)),
                        lon=float(row.get("longitud", 0)),
                    )

                ciudad_obj = ciudades_cache[nombre]

                registro = RegistroClima(
                    ciudad_id         = ciudad_obj.id,
                    temperatura       = float(row["temperatura"]),
                    sensacion_termica = float(row["sensacion_termica"]),
                    humedad           = float(row["humedad"]),
                    velocidad_viento  = float(row["velocidad_viento"]),
                    descripcion       = str(row["descripcion"]),
                    codigo_tiempo     = int(row["codigo_tiempo"]) if pd.notna(row.get("codigo_tiempo")) else None,
                    fecha_extraccion  = row["fecha_extraccion"],
                )
                db.add(registro)
                guardados += 1

            except Exception as e:
                logger.error(f"❌ Error en fila {_}: {e}")
                fallidos += 1

        db.commit()
        logger.info(f"✅ Bulk insert completado: {guardados} registros guardados")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error en commit: {e}")
        guardados = 0
        fallidos = len(df)
    finally:
        db.close()

    return guardados, fallidos


def registrar_metrica(extraidos: int, guardados: int, fallidos: int,
                      segundos: float, estado: str) -> None:
    db = SessionLocal()
    try:
        m = MetricasETL(
            fecha_ejecucion           = datetime.utcnow(),
            estado                    = estado,
            registros_extraidos       = extraidos,
            registros_guardados       = guardados,
            registros_fallidos        = fallidos,
            tiempo_ejecucion_segundos = segundos,
            mensaje                   = f"Carga completada en {segundos:.2f}s",
        )
        db.add(m)
        db.commit()
        logger.info(f"📋 Métrica registrada: {estado}")
    except Exception as e:
        logger.error(f"Error registrando métrica: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    inicio = time.time()
    estado = "exitoso"
    os.makedirs("logs", exist_ok=True)

    try:
        crear_tablas()
        df = cargar_datos()
        guardados, fallidos = bulk_insert(df)

        if fallidos == len(df):
            estado = "error"
        elif fallidos > 0:
            estado = "parcial"

        logger.info(f"✅ ETL completado — Guardados: {guardados} | Fallidos: {fallidos}")

    except Exception as e:
        logger.error(f"Error general: {e}")
        guardados = fallidos = 0
        estado = "error"
        df = pd.DataFrame()

    segundos = round(time.time() - inicio, 2)
    registrar_metrica(len(df), guardados, fallidos, segundos, estado)
    logger.info(f"⏱  Tiempo total: {segundos}s | Estado: {estado}")