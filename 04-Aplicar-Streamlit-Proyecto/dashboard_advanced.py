"""
dashboard_advanced.py - Dashboard avanzado World Bank
Ejecutar: streamlit run dashboard_advanced.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import cargar_datos
from consultas import colombia_vs_latam, ranking_pib_pc, colombia_detalle, balanza_comercial

st.set_page_config(page_title="World Bank Avanzado", page_icon="📊", layout="wide")
st.title("📊 Análisis Avanzado – World Bank PIB")
st.caption("Colombia vs América Latina | 2000-2023")

@st.cache_data
def get_data():
    df = cargar_datos()
    df["anio"] = df["anio"].astype(int)
    return df

df = get_data()

with st.sidebar:
    st.header("⚙️ Configuración")
    anio_sel = st.selectbox("Año para ranking", sorted(df["anio"].unique(), reverse=True))
    paises_sel = st.multiselect("Países", df["pais_nombre"].unique().tolist(),
                                 default=df["pais_nombre"].unique().tolist())

df_f = df[df["pais_nombre"].isin(paises_sel)]

# ── Colombia vs LATAM ─────────────────────────────────────────────────────────
st.subheader("🇨🇴 Colombia vs América Latina")
comp = colombia_vs_latam(df_f)
if not comp.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=comp["anio"], y=comp["colombia"],
                             name="Colombia", line=dict(color="#e94560", width=3)))
    fig.add_trace(go.Scatter(x=comp["anio"], y=comp["latam_promedio"],
                             name="Promedio LATAM", line=dict(color="#0f3460", width=2, dash="dash")))
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.update_layout(title="Crecimiento PIB: Colombia vs LATAM (%)",
                      template="plotly_white", yaxis_title="%", xaxis_title="Año")
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🏆 Ranking PIB Per Cápita ({anio_sel})")
    rank = ranking_pib_pc(df_f, anio_sel)
    if not rank.empty:
        colores = ["#e94560" if p == "Colombia" else "#0f3460" for p in rank["pais_nombre"]]
        fig2 = go.Figure(go.Bar(
            x=rank["pib_per_capita_usd"], y=rank["pais_nombre"],
            orientation="h", marker_color=colores,
            text=rank["pib_per_capita_usd"].apply(lambda x: f"${x:,.0f}"),
            textposition="outside"
        ))
        fig2.update_layout(template="plotly_white", xaxis_title="USD")
        st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("⚖️ Balanza Comercial (% PIB)")
    bal = balanza_comercial(df_f)
    if not bal.empty:
        fig3 = px.line(bal, x="anio", y="balanza", color="pais_nombre",
                       template="plotly_white",
                       labels={"balanza": "% PIB", "anio": "Año"})
        fig3.add_hline(y=0, line_dash="dot", line_color="gray")
        st.plotly_chart(fig3, use_container_width=True)

st.subheader("🔍 Colombia – Todos los Indicadores")
co_det = colombia_detalle(df_f)
if not co_det.empty:
    col3, col4 = st.columns(2)
    with col3:
        fig4 = px.line(co_det.dropna(subset=["inflacion_pct"]), x="anio", y="inflacion_pct",
                       title="Inflación (%)", template="plotly_white")
        fig4.update_traces(line_color="#e74c3c", line_width=2)
        st.plotly_chart(fig4, use_container_width=True)
    with col4:
        fig5 = px.line(co_det.dropna(subset=["desempleo_pct"]), x="anio", y="desempleo_pct",
                       title="Desempleo (%)", template="plotly_white")
        fig5.update_traces(line_color="#3498db", line_width=2)
        st.plotly_chart(fig5, use_container_width=True)

cols = ["anio", "pib_usd", "crecimiento_pib_pct", "pib_per_capita_usd", "inflacion_pct", "desempleo_pct"]
st.dataframe(co_det[[c for c in cols if c in co_det.columns]], use_container_width=True)

