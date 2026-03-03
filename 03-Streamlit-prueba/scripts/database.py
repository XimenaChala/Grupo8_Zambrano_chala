import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Prioriza los Secrets de Streamlit (Nube) sobre el .env (Local)
# IMPORTANTE: La URL debe empezar con postgresql+psycopg:// para usar el driver v3
db_url = st.secrets.get("DATABASE_URL") or os.getenv("DATABASE_URL")

if not db_url:
    st.error("Configuración de base de datos no encontrada.")
    st.stop()

# Crear el engine
engine = create_engine(db_url)

# Crear la fábrica de sesiones (ESTO ES LO QUE FALTA)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()