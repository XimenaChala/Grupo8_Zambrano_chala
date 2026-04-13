#!/usr/bin/env python3
"""
Visualizador de datos - World Bank PIB
Genera gráficas a partir de data/worldbank_pib.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

os.makedirs("data", exist_ok=True)

# ── Cargar datos ──────────────────────────────────────────────────────────────
df = pd.read_csv("data/worldbank_pib.csv")
df = df.dropna(subset=["pib_usd"])

paises = df["pais_codigo"].unique().tolist()
colores = plt.cm.tab10(np.linspace(0, 1, len(paises)))
color_map = dict(zip(paises, colores))

fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.suptitle("Indicadores Económicos - World Bank\nColombia vs Comparados", fontsize=16, fontweight="bold")

# ── Gráfica 1: PIB USD por año ────────────────────────────────────────────────
ax1 = axes[0, 0]
for pais in paises:
    sub = df[df["pais_codigo"] == pais].sort_values("anio")
    lw = 2.5 if pais == "CO" else 1.2
    ls = "-"  if pais == "CO" else "--"
    ax1.plot(sub["anio"], sub["pib_usd"] / 1e12, label=pais, color=color_map[pais], linewidth=lw, linestyle=ls)

ax1.set_title("PIB Total (Billones USD)")
ax1.set_ylabel("PIB (Billones USD)")
ax1.set_xlabel("Año")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}T"))
ax1.legend(fontsize=8)
ax1.grid(alpha=0.3)

# ── Gráfica 2: Crecimiento del PIB (%) ───────────────────────────────────────
ax2 = axes[0, 1]
for pais in paises:
    sub = df[df["pais_codigo"] == pais].dropna(subset=["crecimiento_pib_pct"]).sort_values("anio")
    lw = 2.5 if pais == "CO" else 1.2
    ax2.plot(sub["anio"], sub["crecimiento_pib_pct"], label=pais, color=color_map[pais], linewidth=lw)

ax2.axhline(0, color="black", linewidth=0.8, linestyle=":")
ax2.set_title("Crecimiento del PIB (%)")
ax2.set_ylabel("Crecimiento (%)")
ax2.set_xlabel("Año")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)

# ── Gráfica 3: PIB per cápita ─────────────────────────────────────────────────
ax3 = axes[1, 0]
ultimo_anio = df["anio"].max()
sub_ultimo = df[df["anio"] == ultimo_anio].dropna(subset=["pib_per_capita_usd"])
sub_ultimo = sub_ultimo.sort_values("pib_per_capita_usd", ascending=False)

bars = ax3.bar(sub_ultimo["pais_codigo"], sub_ultimo["pib_per_capita_usd"],
               color=[color_map.get(p, "gray") for p in sub_ultimo["pais_codigo"]])

for bar, pais in zip(bars, sub_ultimo["pais_codigo"]):
    if pais == "CO":
        bar.set_edgecolor("black")
        bar.set_linewidth(2)

ax3.set_title(f"PIB Per Cápita USD ({ultimo_anio})")
ax3.set_ylabel("USD")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax3.grid(axis="y", alpha=0.3)

# ── Gráfica 4: Inflación vs Desempleo Colombia ───────────────────────────────
ax4 = axes[1, 1]
co = df[df["pais_codigo"] == "CO"].dropna(subset=["inflacion_pct", "desempleo_pct"]).sort_values("anio")

ax4.plot(co["anio"], co["inflacion_pct"],  label="Inflación (%)",  color="#e74c3c", linewidth=2)
ax4.plot(co["anio"], co["desempleo_pct"], label="Desempleo (%)", color="#3498db", linewidth=2)
ax4.set_title("Colombia: Inflación vs Desempleo")
ax4.set_ylabel("%")
ax4.set_xlabel("Año")
ax4.legend()
ax4.grid(alpha=0.3)

plt.tight_layout()
out_path = "data/worldbank_graficas.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"✅ Gráficas guardadas en {out_path}")
plt.show()

