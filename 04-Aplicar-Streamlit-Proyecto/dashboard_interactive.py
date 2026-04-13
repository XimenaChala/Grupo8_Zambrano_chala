"""
dashboard_interactive.py ⭐ App principal - World Bank Dashboard
Ejecutar: streamlit run dashboard_interactive.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from database import cargar_datos, test_conexion
from consultas import colombia_vs_latam, ranking_pib_pc, colombia_detalle, balanza_comercial

st.set_page_config(
    page_title="World Bank | Colombia",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 1.4rem; font-weight: 700; }
    .titulo { font-size: 1.2rem; font-weight: 700; color: #0f3460;
              border-bottom: 3px solid #e94560; padding-bottom: 5px; margin-bottom: 15px; }
    .fuente { font-size: 0.75rem; color: #888; }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def get_data():
    df = cargar_datos()
    if not df.empty:
        df["anio"] = df["anio"].astype(int)
    return df

df = get_data()

if df.empty:
    st.error("❌ No se encontraron datos. Ejecuta primero `python scripts/extractor.py`")
    st.stop()

with st.sidebar:
    st.title("🌎 World Bank")
    st.caption("PIB & Crecimiento Económico")

    if test_conexion():
        st.success("🐘 PostgreSQL conectado")
    else:
        st.info("📁 Usando datos CSV")

    st.markdown("---")
    st.header("Filtros")

    anio_min, anio_max = int(df["anio"].min()), int(df["anio"].max())
    rango = st.slider("Rango de años", anio_min, anio_max, (2000, anio_max))

    paises_disponibles = sorted(df["pais_nombre"].unique().tolist())
    paises_sel = st.multiselect("Países", paises_disponibles, default=paises_disponibles)

    st.markdown("---")
    pagina = st.radio("📄 Sección", [
        "📊 Resumen General",
        "🇨🇴 Colombia Detalle",
        "🌎 Comparativa Regional",
        "⚖️ Balanza Comercial",
    ])

df_f = df[
    (df["anio"] >= rango[0]) &
    (df["anio"] <= rango[1]) &
    (df["pais_nombre"].isin(paises_sel))
]
co = df_f[df_f["pais_codigo"] == "CO"].sort_values("anio")

# ══════════════════════════════════════════════════════
# PÁGINA 1: RESUMEN GENERAL
# ══════════════════════════════════════════════════════
if pagina == "📊 Resumen General":
    st.title("📊 Resumen General – Indicadores Económicos")

    ultimo    = co.iloc[-1] if not co.empty else pd.Series()
    penultimo = co.iloc[-2] if len(co) > 1 else pd.Series()

    # PIB con manejo de NaN
    pib_val = ultimo.get('pib_usd')
    pib_str = f"${pib_val/1e9:.1f}B" if pib_val and not pd.isna(pib_val) else "N/D"

    # Crecimiento con manejo de NaN
    crec_val  = ultimo.get('crecimiento_pib_pct', 0) or 0
    crec_prev = penultimo.get('crecimiento_pib_pct', 0) or 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🇨🇴 PIB Colombia",
              pib_str,
              f"Año {int(ultimo.get('anio', 0))}")
    c2.metric("📈 Crecimiento PIB",
              f"{crec_val:.1f}%",
              f"{crec_val - crec_prev:+.1f}pp")
    c3.metric("💸 Inflación",  f"{ultimo.get('inflacion_pct', 0) or 0:.1f}%")
    c4.metric("👷 Desempleo",  f"{ultimo.get('desempleo_pct', 0) or 0:.1f}%")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p class="titulo">Evolución PIB Total</p>', unsafe_allow_html=True)
        fig = px.line(df_f.dropna(subset=["pib_usd"]), x="anio", y="pib_usd",
                      color="pais_nombre", template="plotly_white",
                      labels={"pib_usd": "PIB (USD)", "anio": "Año", "pais_nombre": "País"})
        fig.update_layout(yaxis_tickformat=".2s")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="titulo">Crecimiento PIB (%)</p>', unsafe_allow_html=True)
        fig2 = px.line(df_f.dropna(subset=["crecimiento_pib_pct"]), x="anio",
                       y="crecimiento_pib_pct", color="pais_nombre", template="plotly_white",
                       labels={"crecimiento_pib_pct": "%", "anio": "Año"})
        fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════
# PÁGINA 2: COLOMBIA DETALLE
# ══════════════════════════════════════════════════════
elif pagina == "🇨🇴 Colombia Detalle":
    st.title("🇨🇴 Colombia – Análisis Detallado")
    co_det = colombia_detalle(df_f)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(co_det.dropna(subset=["pib_usd"]), x="anio", y="pib_usd",
                      title="PIB Total Colombia (USD)", template="plotly_white",
                      labels={"pib_usd": "USD", "anio": "Año"})
        fig.update_traces(fillcolor="rgba(233,69,96,0.2)", line_color="#e94560")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=co_det["anio"], y=co_det["inflacion_pct"],
                                  name="Inflación", line=dict(color="#e74c3c", width=2)))
        fig2.add_trace(go.Scatter(x=co_det["anio"], y=co_det["desempleo_pct"],
                                  name="Desempleo", line=dict(color="#3498db", width=2)))
        fig2.update_layout(title="Inflación vs Desempleo (%)", template="plotly_white",
                           yaxis_title="%", xaxis_title="Año")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Tabla de datos Colombia")
    cols_show = ["anio", "pib_usd", "crecimiento_pib_pct", "pib_per_capita_usd",
                 "inflacion_pct", "desempleo_pct", "exportaciones_pct_pib", "importaciones_pct_pib"]
    st.dataframe(co_det[[c for c in cols_show if c in co_det.columns]], use_container_width=True)
    csv = co_det.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar CSV Colombia", csv, "colombia_indicadores.csv")

# ══════════════════════════════════════════════════════
# PÁGINA 3: COMPARATIVA REGIONAL
# ══════════════════════════════════════════════════════
elif pagina == "🌎 Comparativa Regional":
    st.title("🌎 Comparativa Regional")

    anio_rank = st.selectbox("Año para ranking", sorted(df_f["anio"].unique(), reverse=True))

    col1, col2 = st.columns(2)
    with col1:
        comp = colombia_vs_latam(df_f)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=comp["anio"], y=comp["colombia"],
                                 name="Colombia", line=dict(color="#e94560", width=3)))
        fig.add_trace(go.Scatter(x=comp["anio"], y=comp["latam_promedio"],
                                 name="Promedio LATAM", line=dict(color="#0f3460", width=2, dash="dash")))
        fig.add_hline(y=0, line_dash="dot", line_color="gray")
        fig.update_layout(title="Colombia vs Promedio LATAM (%)",
                          template="plotly_white", yaxis_title="%", xaxis_title="Año")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rank = ranking_pib_pc(df_f, anio_rank)
        colores = ["#e94560" if p == "Colombia" else "#0f3460" for p in rank["pais_nombre"]]
        fig2 = go.Figure(go.Bar(
            x=rank["pib_per_capita_usd"], y=rank["pais_nombre"],
            orientation="h", marker_color=colores,
            text=rank["pib_per_capita_usd"].apply(lambda x: f"${x:,.0f}"),
            textposition="outside"
        ))
        fig2.update_layout(title=f"PIB Per Cápita ({anio_rank})",
                           template="plotly_white", xaxis_title="USD")
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════
# PÁGINA 4: BALANZA COMERCIAL
# ══════════════════════════════════════════════════════
elif pagina == "⚖️ Balanza Comercial":
    st.title("⚖️ Balanza Comercial")

    bal = balanza_comercial(df_f)
    fig = px.line(bal, x="anio", y="balanza", color="pais_nombre",
                  title="Balanza Comercial (Exportaciones - Importaciones) % PIB",
                  template="plotly_white", labels={"balanza": "% PIB", "anio": "Año"})
    fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.4,
                  annotation_text="Equilibrio")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig2 = px.bar(df_f.dropna(subset=["exportaciones_pct_pib"]), x="anio",
                      y="exportaciones_pct_pib", color="pais_nombre", barmode="group",
                      title="Exportaciones (% PIB)", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        fig3 = px.bar(df_f.dropna(subset=["importaciones_pct_pib"]), x="anio",
                      y="importaciones_pct_pib", color="pais_nombre", barmode="group",
                      title="Importaciones (% PIB)", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown('<p class="fuente">Fuente: World Bank Open Data | https://data.worldbank.org | Grupo 8 – Zambrano & Chala</p>',
            unsafe_allow_html=True)
