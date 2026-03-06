"""
test_db.py - Prueba la conexión a PostgreSQL y verifica los datos
Ejecutar: python scripts/test_db.py
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import test_conexion, cargar_datos, get_engine
from sqlalchemy import text


def test_conexion_db():
    print("\n🔌 Test 1: Conexión a PostgreSQL")
    if test_conexion():
        print("  ✅ Conexión exitosa")
        return True
    else:
        print("  ⚠️  Sin conexión — se usará CSV como fallback")
        return False


def test_carga_datos():
    print("\n📊 Test 2: Carga de datos")
    df = cargar_datos()
    if df.empty:
        print("  ❌ No se encontraron datos")
        return
    print(f"  ✅ {len(df)} filas cargadas")
    print(f"  Países: {df['pais_codigo'].unique().tolist()}")
    print(f"  Años: {df['anio'].min()} - {df['anio'].max()}")


def test_consulta_colombia():
    print("\n🇨🇴 Test 3: Datos Colombia")
    df = cargar_datos()
    co = df[df["pais_codigo"] == "CO"]
    if co.empty:
        print("  ❌ Sin datos de Colombia")
        return
    ultimo = co.sort_values("anio").iloc[-1]
    print(f"  ✅ Último año: {int(ultimo['anio'])}")
    print(f"  PIB per cápita: ${ultimo.get('pib_per_capita_usd', 0):,.0f} USD")
    print(f"  Crecimiento PIB: {ultimo.get('crecimiento_pib_pct', 0):.2f}%")


def test_vistas_postgres():
    print("\n👁️  Test 4: Vistas PostgreSQL")
    if not test_conexion():
        pass
