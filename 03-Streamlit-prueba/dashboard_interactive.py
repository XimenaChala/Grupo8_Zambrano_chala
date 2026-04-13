#!/usr/bin/env python3
import os, sys
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(
    page_title="Dashboard Clima ETL",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ Dashboard Interactivo - Clima Weatherstack")
st.markdown("---")

@st.cache_data(ttl=300)
def cargar_datos() -> pd.DataFrame:
    # Intentar conexión a DB
    try:
        from scripts.database import engine
        df = pd.read_sql("SELECT * FROM clima ORDER BY fecha_extraccion DESC;", engine)
        if not df.empty:
            return df
    except Exception:
        pass
    # Respaldo: CSV local
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'clima.csv')
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()

df = cargar_datos()

if df.empty:
    st.error("❌ No hay datos disponibles. Ejecuta el extractor primero.")
    st.stop()

df.columns = [c.lower() for c in df.columns]
df["fecha_extraccion"] = pd.to_datetime(df["fecha_extraccion"])

# ── Sidebar ─────────────────────────────────────────────────────
st.sidebar.markdown("### 🔧 Filtros")

ciudades = sorted(df["ciudad"].unique().tolist())
ciudades_sel = st.sidebar.multiselect("🏙️ Ciudades", ciudades, default=ciudades)

fecha_min = df["fecha_extraccion"].min().date()
fecha_max = df["fecha_extraccion"].max().date()

fecha_inicio = st.sidebar.date_input("📅 Desde", value=fecha_min)
fecha_fin    = st.sidebar.date_input("📅 Hasta", value=fecha_max)

temp_min = st.sidebar.slider("🌡️ Temp Mín (°C)", -50, 50, int(df["temperatura"].min()) - 1)
temp_max = st.sidebar.slider("🌡️ Temp Máx (°C)", -50, 50, int(df["temperatura"].max()) + 1)

# ── Filtros ──────────────────────────────────────────────────────
df_f = df[
    (df["ciudad"].isin(ciudades_sel)) &
    (df["fecha_extraccion"].dt.date >= fecha_inicio) &
    (df["fecha_extraccion"].dt.date <= fecha_fin) &
    (df["temperatura"] >= temp_min) &
    (df["temperatura"] <= temp_max)
]

if df_f.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ── KPIs ─────────────────────────────────────────────────────────
st.markdown("### 📊 Indicadores Clave")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🌡️ Temp Máx",    f"{df_f['temperatura'].max():.1f}°C")
c2.metric("🌡️ Temp Mín",    f"{df_f['temperatura'].min():.1f}°C")
c3.metric("🌡️ Temp Prom",   f"{df_f['temperatura'].mean():.1f}°C")
c4.metric("💧 Humedad Prom", f"{df_f['humedad'].mean():.1f}%")
c5.metric("💨 Viento Máx",  f"{df_f['velocidad_viento'].max():.1f} km/h")

st.markdown("---")

# ── Gráficas ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    fig = px.box(df_f, x="ciudad", y="temperatura", color="ciudad",
                 title="Distribución de Temperatura por Ciudad")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    hum = df_f.groupby("ciudad")["humedad"].mean().reset_index()
    fig = px.bar(hum, x="ciudad", y="humedad", color="humedad",
                 color_continuous_scale="Blues",
                 title="Humedad Promedio por Ciudad")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

temp_t = df_f.groupby(["fecha_extraccion", "ciudad"])["temperatura"].mean().reset_index()
fig = px.line(temp_t, x="fecha_extraccion", y="temperatura", color="ciudad",
              title="Evolución de Temperatura en el Tiempo", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Tabla + descarga ──────────────────────────────────────────────
st.markdown("### 📋 Datos Detallados")
st.dataframe(df_f, use_container_width=True)

st.download_button(
    label="⬇️ Descargar CSV",
    data=df_f.to_csv(index=False),
    file_name=f"clima_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)
