#!/usr/bin/env python3
"""
Extractor DB: Extrae datos de Weatherstack y los carga directamente a PostgreSQL.
Uso local: python scripts/extractor_db.py
"""
import os, sys, time, logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.extractor import WeatherstackExtractor
from scripts.database import SessionLocal, engine
from scripts.models import Base, RegistroClima, MetricasETL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def cargar_a_db(datos: list[dict]) -> tuple[int, int]:
    """Inserta los registros en la tabla clima. Retorna (guardados, fallidos)."""
    db = SessionLocal()
    guardados = fallidos = 0
    try:
        for d in datos:
            try:
                registro = RegistroClima(
                    ciudad            = d['ciudad'],
                    pais              = d['pais'],
                    latitud           = float(d['latitud']),
                    longitud          = float(d['longitud']),
                    temperatura       = d['temperatura'],
                    sensacion_termica = d['sensacion_termica'],
                    humedad           = d['humedad'],
                    velocidad_viento  = d['velocidad_viento'],
                    descripcion       = d['descripcion'],
                    fecha_extraccion  = datetime.strptime(d['fecha_extraccion'], '%Y-%m-%d %H:%M:%S'),
                    codigo_tiempo     = d['codigo_tiempo']
                )
                db.add(registro)
                guardados += 1
            except Exception as e:
                logger.error(f"❌ Error insertando {d.get('ciudad')}: {e}")
                fallidos += 1

        db.commit()
        logger.info(f"✅ {guardados} registros guardados en DB")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error en commit: {e}")
    finally:
        db.close()
    return guardados, fallidos


def registrar_metrica(extraidos, guardados, fallidos, segundos, estado):
    db = SessionLocal()
    try:
        m = MetricasETL(
            fecha_ejecucion           = datetime.utcnow(),
            estado                    = estado,
            registros_extraidos       = extraidos,
            registros_guardados       = guardados,
            registros_fallidos        = fallidos,
            tiempo_ejecucion_segundos = segundos
        )
        db.add(m)
        db.commit()
    except Exception as e:
        logger.error(f"Error registrando métrica: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    inicio = time.time()
    estado = "exitoso"

    try:
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)

        ext   = WeatherstackExtractor()
        datos = ext.ejecutar()

        if datos:
            guardados, fallidos = cargar_a_db(datos)
        else:
            guardados = fallidos = 0
            estado = "sin_datos"

    except Exception as e:
        logger.error(f"Error general: {e}")
        guardados = fallidos = 0
        estado = "error"

    segundos = round(time.time() - inicio, 2)
    registrar_metrica(len(datos) if datos else 0, guardados, fallidos, segundos, estado)
    logger.info(f"⏱ Tiempo total: {segundos}s | Estado: {estado}")
