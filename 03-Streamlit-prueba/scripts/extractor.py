#!/usr/bin/env python3
"""
Extractor: Consulta la API de Weatherstack y guarda los datos en CSV y JSON.
Uso local: python scripts/extractor.py
"""
import os, time, json, logging
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WeatherstackExtractor:
    def __init__(self):
        self.api_key  = os.getenv('API_KEY')
        self.base_url = os.getenv('WEATHERSTACK_BASE_URL', 'http://api.weatherstack.com')
        self.ciudades = os.getenv('CIUDADES', 'Bogota').split(',')

        if not self.api_key:
            raise ValueError("API_KEY no configurada en .env")

    def extraer_ciudad(self, ciudad: str) -> dict | None:
        try:
            response = requests.get(
                f"{self.base_url}/current",
                params={'access_key': self.api_key, 'query': ciudad.strip()},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                logger.error(f"❌ Error API ({ciudad}): {data['error']['info']}")
                return None

            logger.info(f"✅ Datos extraídos: {ciudad}")
            return data

        except Exception as e:
            logger.error(f"❌ Error conexión ({ciudad}): {e}")
            return None

    def procesar(self, data: dict) -> dict | None:
        try:
            curr = data.get('current', {})
            loc  = data.get('location', {})
            return {
                'ciudad':            loc.get('name'),
                'pais':              loc.get('country'),
                'latitud':           loc.get('lat'),
                'longitud':          loc.get('lon'),
                'temperatura':       curr.get('temperature'),
                'sensacion_termica': curr.get('feelslike'),
                'humedad':           curr.get('humidity'),
                'velocidad_viento':  curr.get('wind_speed'),
                'descripcion':       curr.get('weather_descriptions', ['N/A'])[0],
                'fecha_extraccion':  datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'codigo_tiempo':     curr.get('weather_code')
            }
        except Exception as e:
            logger.error(f"Error procesando dato: {e}")
            return None

    def ejecutar(self) -> list[dict]:
        logger.info(f"Iniciando extracción para {len(self.ciudades)} ciudades...")
        resultados = []
        for ciudad in self.ciudades:
            dato = self.extraer_ciudad(ciudad)
            if dato:
                procesado = self.procesar(dato)
                if procesado:
                    resultados.append(procesado)
            time.sleep(2)  # evita error 429 en plan FREE
        return resultados


if __name__ == "__main__":
    ext    = WeatherstackExtractor()
    datos  = ext.ejecutar()

    if datos:
        os.makedirs('data', exist_ok=True)

        with open('data/clima_raw.json', 'w') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        logger.info("📁 Guardado: data/clima_raw.json")

        df = pd.DataFrame(datos)
        df.to_csv('data/clima.csv', index=False)
        logger.info("📁 Guardado: data/clima.csv")
    else:
        logger.warning("⚠️ No se obtuvieron datos.")
