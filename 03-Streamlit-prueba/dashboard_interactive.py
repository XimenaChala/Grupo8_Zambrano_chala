#!/usr/bin/env python3
import streamlit as st
import pandas as pd
from scripts.database import engine
import plotly.express as px
from datetime import datetime, timedelta

# ------------------- Configuración -------------------
st.set_page_config(
    page_title="Dashboard Interactivo",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ Dashboard Interactivo - Clima Weatherstack")
st.markdown("---")

# ------------------- Leer datos desde PostgreSQL -------------------
df = pd.read_sql("SELECT * FROM clima;", engine)

if df.empty:
    st.warning("⚠️ No hay datos en la base de datos")
    st.stop()

# Convertir fecha
df["fecha_extraccion"] = pd.to_datetime(df["fecha_extraccion"])

# ------------------- Sidebar -------------------
st.sidebar.markdown("### 🔧 Filtros")

ciudades = df["ciudad"].unique().tolist()

ciudades_seleccionadas = st.sidebar.multiselect(
    "🏙️ Ciudades",
    options=ciudades,
    default=ciudades
)

fecha_inicio = st.sidebar.date_input(
    "📅 Desde",
    value=df["fecha_extraccion"].min().date()
)

fecha_fin = st.sidebar.date_input(
    "📅 Hasta",
    value=df["fecha_extraccion"].max().date()
)

temp_min = st.sidebar.slider("🌡️ Temp Mín", -50, 50, -10)
temp_max = st.sidebar.slider("🌡️ Temp Máx", -50, 50, 40)

# ------------------- Aplicar filtros -------------------
df_filtrado = df[
    (df["ciudad"].isin(ciudades_seleccionadas)) &
    (df["fecha_extraccion"].dt.date >= fecha_inicio) &
    (df["fecha_extraccion"].dt.date <= fecha_fin) &
    (df["temperatura"] >= temp_min) &
    (df["temperatura"] <= temp_max)
]

if df_filtrado.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados")
    st.stop()

# ------------------- KPIs -------------------
st.markdown("### 📊 Indicadores Clave")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🌡️ Temp Max", f"{df_filtrado['temperatura'].max():.1f}°C")

with col2:
    st.metric("🌡️ Temp Min", f"{df_filtrado['temperatura'].min():.1f}°C")

with col3:
    st.metric("🌡️ Temp Prom", f"{df_filtrado['temperatura'].mean():.1f}°C")

with col4:
    st.metric("💧 Humedad Prom", f"{df_filtrado['humedad'].mean():.1f}%")

with col5:
    st.metric("💨 Viento Max", f"{df_filtrado['velocidad_viento'].max():.1f} km/h")

st.markdown("---")

# ------------------- Gráficas -------------------
col1, col2 = st.columns(2)

with col1:
    fig_temp = px.box(
        df_filtrado,
        x="ciudad",
        y="temperatura",
        color="ciudad",
        title="Distribución de Temperatura por Ciudad"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    humedad_ciudad = df_filtrado.groupby("ciudad")["humedad"].mean().reset_index()
    fig_hum = px.bar(
        humedad_ciudad,
        x="ciudad",
        y="humedad",
        color="humedad",
        color_continuous_scale="Blues",
        title="Humedad Promedio por Ciudad"
    )
    st.plotly_chart(fig_hum, use_container_width=True)

st.markdown("---")

# Evolución temporal
temp_tiempo = df_filtrado.groupby(
    ["fecha_extraccion", "ciudad"]
)["temperatura"].mean().reset_index()

fig_line = px.line(
    temp_tiempo,
    x="fecha_extraccion",
    y="temperatura",
    color="ciudad",
    title="Evolución de Temperatura en el Tiempo",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# ------------------- Tabla -------------------
st.markdown("### 📋 Datos Detallados")

st.dataframe(df_filtrado, use_container_width=True)

# Descargar CSV
csv = df_filtrado.to_csv(index=False)

st.download_button(
    label="⬇️ Descargar CSV",
    data=csv,
    file_name=f"clima_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)
