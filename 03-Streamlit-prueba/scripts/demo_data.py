#!/usr/bin/env python3
"""
demo_data.py — Genera 1000 registros sintéticos de clima para 5 ciudades colombianas.
Uso: python scripts/demo_data.py
Salida: data/clima_raw.json  y  data/clima.csv
"""
import os
import json
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

# Configuración por ciudad (temperatura base, humedad base, viento base)
CIUDADES = {
    "Bogota":       {"pais": "Colombia", "lat": "4.600",  "lon": "-74.083", "temp_base": 14, "hum_base": 80, "viento_base": 10},
    "Medellin":     {"pais": "Colombia", "lat": "6.291",  "lon": "-75.536", "temp_base": 22, "hum_base": 70, "viento_base": 8},
    "Cali":         {"pais": "Colombia", "lat": "3.437",  "lon": "-76.523", "temp_base": 26, "hum_base": 65, "viento_base": 7},
    "Barranquilla": {"pais": "Colombia", "lat": "10.964", "lon": "-74.796", "temp_base": 30, "hum_base": 72, "viento_base": 20},
    "Cartagena":    {"pais": "Colombia", "lat": "10.400", "lon": "-75.514", "temp_base": 29, "hum_base": 75, "viento_base": 18},
}

DESCRIPCIONES = [
    "Partly cloudy", "Clear", "Overcast",
    "Patchy rain nearby", "Sunny", "Light rain"
]

CODIGOS = {
    "Partly cloudy": 116, "Clear": 113, "Overcast": 122,
    "Patchy rain nearby": 176, "Sunny": 113, "Light rain": 296
}

def generar_registro(ciudad, config, fecha):
    temp = round(config["temp_base"] + random.uniform(-6, 6), 1)
    hum  = min(100, max(30, int(config["hum_base"] + random.uniform(-15, 15))))
    viento = max(1, int(config["viento_base"] + random.uniform(-5, 15)))
    # Sensación térmica: fórmula simplificada
    sensacion = round(temp + (hum / 100) * 2 - (viento / 10), 1)
    descripcion = random.choice(DESCRIPCIONES)
    return {
        "ciudad":            ciudad,
        "pais":              config["pais"],
        "latitud":           config["lat"],
        "longitud":          config["lon"],
        "temperatura":       temp,
        "sensacion_termica": sensacion,
        "humedad":           hum,
        "velocidad_viento":  viento,
        "descripcion":       descripcion,
        "fecha_extraccion":  fecha.strftime("%Y-%m-%d %H:%M:%S"),
        "codigo_tiempo":     CODIGOS[descripcion],
    }

def main():
    os.makedirs("data", exist_ok=True)

    registros = []
    fecha_inicio = datetime.now() - timedelta(days=30)

    # 200 registros por ciudad = 1000 total
    for ciudad, config in CIUDADES.items():
        for i in range(200):
            fecha = fecha_inicio + timedelta(hours=i * 3.6)
            registros.append(generar_registro(ciudad, config, fecha))

    # Mezclar aleatoriamente
    random.shuffle(registros)

    # Guardar JSON
    with open("data/clima_raw.json", "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)

    # Guardar CSV
    df = pd.DataFrame(registros)
    df.to_csv("data/clima.csv", index=False)

    print(f"✅ {len(registros)} registros sintéticos generados")
    print(f"   📁 data/clima_raw.json")
    print(f"   📁 data/clima.csv")
    print(f"\n📊 Distribución por ciudad:")
    print(df["ciudad"].value_counts().to_string())

if __name__ == "__main__":
    main()