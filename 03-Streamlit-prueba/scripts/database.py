import os
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Prioriza los Secrets de Streamlit (Nube) sobre el .env (Local)
db_url = st.secrets.get("DATABASE_URL") or os.getenv("DATABASE_URL")

if db_url:
    engine = create_engine(db_url)
else:
    # Si no hay DB, podemos hacer que el dashboard no falle y use datos locales
    engine = None