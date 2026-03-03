import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Obtiene la URL: primero Streamlit Secrets (nube), luego .env (local)"""
    try:
        import streamlit as st
        url = st.secrets.get("DATABASE_URL")
        if url:
            return url
    except Exception:
        pass
    return os.getenv("DATABASE_URL")

db_url = get_database_url()

if not db_url:
    raise ValueError("❌ DATABASE_URL no encontrada en secrets ni en .env")

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
