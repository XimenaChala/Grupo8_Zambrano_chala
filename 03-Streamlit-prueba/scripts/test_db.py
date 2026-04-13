#!/usr/bin/env python3
"""
Prueba de conexión a la base de datos.
Uso: python scripts/test_db.py
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from scripts.database import engine

print("--- Prueba de Conexión ---")
try:
    with engine.connect() as conn:
        row = conn.execute(text("SELECT current_database(), current_user;")).fetchone()
        print(f"✅ Conexión exitosa")
        print(f"   Base de datos : {row[0]}")
        print(f"   Usuario       : {row[1]}")
except Exception as e:
    print(f"❌ Falló la conexión: {e}")
