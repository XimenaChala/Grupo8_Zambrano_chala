#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Añadir el path para encontrar los scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Configuración de la página (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="Dashboard de Clima ETL",
    page_icon="🌡️",
    layout="wide"
)

# --- LÓGICA DE CARGA DE DATOS (Híbrida Nube/Local) ---
@st.cache_data
def cargar_datos():
    # Intentar conexión a Base de Datos
    try:
        from scripts.database import engine
        return pd.read_sql("SELECT * FROM clima", engine)
    except Exception:
        # Si la DB falla (como en la nube), cargar el respaldo CSV
        csv_path = '03-Streamlit-prueba/data/clima.csv'
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            return None

# Título principal
st.title("🌍 Dashboard de Clima - ETL Weatherstack")
st.markdown("---")

df = cargar_datos()

if df is None or df.empty:
    st.error("❌ No se pudieron encontrar datos en la Base de Datos ni en el CSV de respaldo.")
    st.info("Asegúrate de haber ejecutado los scripts de extracción y carga localmente.")
    st.stop()

# --- SIDEBAR CON FILTROS ---
st.sidebar.title("🔧 Filtros")

# Normalizar nombres de columnas por si vienen de CSV o SQL
if 'ciudad' in df.columns: df = df.rename(columns={'ciudad': 'Ciudad', 'temperatura': 'Temperatura', 'humedad': 'Humedad', 'velocidad_viento': 'Viento'})

ciudades_filtro = st.sidebar.multiselect(
    "Selecciona Ciudades:",
    options=df['Ciudad'].unique(),
    default=df['Ciudad'].unique()
)

df_filtrado = df[df['Ciudad'].isin(ciudades_filtro)]

# --- MÉTRICAS ---
st.subheader("📈 Métricas Principales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌡️ Temp. Promedio", f"{df_filtrado['Temperatura'].mean():.1f}°C")
with col2:
    st.metric("💧 Humedad Promedio", f"{df_filtrado['Humedad'].mean():.1f}%")
with col3:
    st.metric("💨 Viento Máximo", f"{df_filtrado['Viento'].max():.1f} km/h")
with col4:
    st.metric("📊 Total Registros", len(df_filtrado))

# --- GRÁFICAS ---
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    fig_temp = px.bar(df_filtrado, x='Ciudad', y='Temperatura', title="Temperatura por Ciudad", color='Temperatura', color_continuous_scale='RdYlBu_r')
    st.plotly_chart(fig_temp, use_container_width=True)

with c2:
    fig_humid = px.bar(df_filtrado, x='Ciudad', y='Humedad', title="Humedad por Ciudad", color='Humedad', color_continuous_scale='Blues')
    st.plotly_chart(fig_humid, use_container_width=True)

# Tabla detallada
st.subheader("📋 Datos Detallados")
st.dataframe(df_filtrado, use_container_width=True)