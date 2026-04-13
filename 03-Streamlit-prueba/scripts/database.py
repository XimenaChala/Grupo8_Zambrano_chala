import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Obtiene la URL: primero .env (local), luego Streamlit Secrets (nube)"""
    # Intento 1: variables de entorno / .env (desarrollo local)
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    
    # Intento 2: Streamlit Secrets (solo en Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'DATABASE_URL' in st.secrets:
            return st.secrets.get("DATABASE_URL")
    except Exception:
        pass
    
    return None

db_url = get_database_url()

if not db_url:
    raise ValueError("❌ DATABASE_URL no encontrada en secrets ni en .env")

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()