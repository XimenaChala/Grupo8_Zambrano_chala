#!/usr/bin/env python3
import os
import requests
import json
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
import logging

# Configuración inicial
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/etl.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class WeatherstackExtractor:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = os.getenv('WEATHERSTACK_BASE_URL')
        # Obtiene la lista de ciudades del archivo .env
        self.ciudades = os.getenv('CIUDADES', 'Bogota').split(',')
        
        if not self.api_key:
            raise ValueError("API_KEY no encontrada en el archivo .env")

    def extraer_clima(self, ciudad):
        """Consulta la API para una ciudad específica"""
        try:
            url = f"{self.base_url}/current"
            params = {'access_key': self.api_key, 'query': ciudad.strip()}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                logger.error(f"❌ Error API ({ciudad}): {data['error']['info']}")
                return None
            
            logger.info(f"✅ Datos extraídos: {ciudad}")
            return data
        except Exception as e:
            logger.error(f"❌ Error de conexión ({ciudad}): {str(e)}")
            return None

    def procesar_dato(self, data):
        """Mapea el JSON crudo al formato de la base de datos"""
        try:
            curr = data.get('current', {})
            loc = data.get('location', {})
            return {
                'ciudad': loc.get('name'),
                'pais': loc.get('country'),
                'latitud': loc.get('lat'),
                'longitud': loc.get('lon'),
                'temperatura': curr.get('temperature'),
                'sensacion_termica': curr.get('feelslike'),
                'humedad': curr.get('humidity'),
                'velocidad_viento': curr.get('wind_speed'),
                'descripcion': curr.get('weather_descriptions', ['N/A'])[0],
                'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'codigo_tiempo': curr.get('weather_code')
            }
        except Exception as e:
            logger.error(f"Error procesando JSON: {str(e)}")
            return None

    def ejecutar(self):
        resultados = []
        for ciudad in self.ciudades:
            res = self.extraer_clima(ciudad)
            if res:
                procesado = self.procesar_dato(res)
                if procesado: resultados.append(procesado)
            
            # Pausa crítica para evitar Error 429 en cuentas gratuitas
            time.sleep(2) 
        return resultados

if __name__ == "__main__":
    ext = WeatherstackExtractor()
    lista_clima = ext.ejecutar()
    if lista_clima:
        df = pd.DataFrame(lista_clima)
        # Guarda el respaldo en CSV que usará el cargador
        df.to_csv('data/clima.csv', index=False)
        logger.info("📁 Archivo data/clima.csv actualizado con éxito.")