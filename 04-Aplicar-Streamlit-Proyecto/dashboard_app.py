"""
dashboard_app.py - Dashboard básico World Bank
Ejecutar: streamlit run dashboard_app.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

import streamlit as st
import pandas as pd
import plotly.express as px
from database import cargar_datos

st.set_page_config(page_title="World Bank - Dashboard", page_icon="🌎", layout="wide")
st.title("🌎 World Bank – PIB Colombia y América Latina")

@st.cache_data
def get_data():
    df = cargar_datos()
    df["anio"] = df["anio"].astype(int)
    return df

df = get_data()

with st.sidebar:
    st.header("Filtros")
    anio_min, anio_max = int(df["anio"].min()), int(df["anio"].max())
    rango = st.slider("Rango de años", anio_min, anio_max, (2000, anio_max))
    paises = st.multiselect("Países", df["pais_nombre"].unique().tolist(),
                             default=df["pais_nombre"].unique().tolist())

df_f = df[(df["anio"] >= rango[0]) & (df["anio"] <= rango[1]) & (df["pais_nombre"].isin(paises))]

co = df_f[df_f["pais_codigo"] == "CO"].sort_values("anio")
ultimo = co.iloc[-1] if not co.empty else {}

col1, col2, col3 = st.columns(3)
col1.metric("PIB Colombia",    f"${ultimo.get('pib_usd', 0)/1e9:.1f}B USD")
col2.metric("Crecimiento PIB", f"{ultimo.get('crecimiento_pib_pct', 0):.1f}%")
col3.metric("PIB Per Cápita",  f"${ultimo.get('pib_per_capita_usd', 0):,.0f}")

fig1 = px.line(df_f.dropna(subset=["crecimiento_pib_pct"]), x="anio",
               y="crecimiento_pib_pct", color="pais_nombre",
               title="Crecimiento PIB (%)", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df_f.dropna(subset=["pib_per_capita_usd"]), x="anio",
               y="pib_per_capita_usd", color="pais_nombre",
               title="PIB Per Cápita (USD)", template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)
