# 📦 02 - ETL Proyecto API – World Bank PIB

Pipeline ETL completo que extrae indicadores económicos de la **World Bank API** para Colombia y países comparados.

## 👥 Grupo 8 – Ximena del pilar zambrano chala

---

## 🔄 ¿Qué es ETL?

| Letra | Significado | Script | ¿Qué hace? |
|-------|-------------|--------|------------|
| **E** | Extract | `extractor.py` | Llama a la API del World Bank y descarga los datos |
| **T** | Transform | `transformador.py` | Limpia, organiza y enriquece los datos |
| **L** | Load | `extractor.py` | Guarda los datos en CSV, JSON y PostgreSQL |

---

## 🌐 API Utilizada

**World Bank API** — `https://api.worldbank.org/v2/`

- ✅ Gratuita y sin API Key
- ✅ Datos económicos de todos los países del mundo desde los años 60
- ✅ Documentación: https://data.worldbank.org/developers

---

## 📊 Indicadores Extraídos

Para **Colombia, USA, Brasil, México, Argentina, Chile y Perú** entre **2000 y 2023**:

| Código World Bank | Descripción |
|-------------------|-------------|
| NY.GDP.MKTP.CD | PIB total en USD |
| NY.GDP.MKTP.KD.ZG | Crecimiento del PIB (%) |
| NY.GDP.PCAP.CD | PIB per cápita USD |
| NY.GDP.PCAP.KD.ZG | Crecimiento PIB per cápita (%) |
| FP.CPI.TOTL.ZG | Inflación (%) |
| SL.UEM.TOTL.ZS | Desempleo (%) |
| NE.EXP.GNFS.ZS | Exportaciones % del PIB |
| NE.IMP.GNFS.ZS | Importaciones % del PIB |

**Resultado: 168 registros limpios extraídos exitosamente**

---

## 🌍 Países Analizados

| Código | País | Rol |
|--------|------|-----|
| CO | Colombia | **País foco** |
| US | United States | Referencia |
| BR | Brazil | América Latina |
| MX | Mexico | América Latina |
| AR | Argentina | América Latina |
| CL | Chile | América Latina |
| PE | Peru | América Latina |

---

## 📁 Estructura del Proyecto
```
02-Elt-Proyecto-Api/
├── .gitignore
├── .env                  ← NO commitear (credenciales BD)
├── requirements.txt
├── README.md
├── venv/                 ← Entorno virtual (NO commitear)
├── data/
│   ├── worldbank_pib.csv
│   ├── worldbank_pib_raw.json
│   └── worldbank_graficas.png
├── scripts/
│   ├── extractor.py      ← EXTRACT + LOAD
│   ├── transformador.py  ← TRANSFORM
│   └── visualizador.py   ← Gráficas con matplotlib
└── logs/
    └── etl.log
```

---

## 📄 Descripción de Archivos

**`scripts/extractor.py`** — Corazón del proyecto. Contiene 3 clases:
- `WorldBankExtractor` — llama la API y descarga los datos
- `WorldBankTransformer` — limpia y enriquece el DataFrame
- `WorldBankLoader` — guarda en CSV, JSON y PostgreSQL

**`scripts/transformador.py`** — Limpia nulos, redondea decimales, clasifica países por región, marca Colombia como país foco y calcula la balanza comercial.

**`scripts/visualizador.py`** — Genera 4 gráficas con matplotlib:
- Evolución del PIB total
- Crecimiento del PIB (%)
- Ranking PIB per cápita
- Inflación vs Desempleo Colombia

**`scripts/crear_bd.sql`** — Diseño de la base de datos PostgreSQL con tablas, índices y vistas. Se usará en la fase 04.

**`requirements.txt`** — Librerías necesarias: requests, pandas, matplotlib, sqlalchemy, psycopg2.

**`.env`** — Credenciales de PostgreSQL. ⚠️ Nunca se sube a GitHub.

---

## 🗄️ Base de Datos PostgreSQL (Fase 04)

Diseñada con la tabla `indicadores_pib` y dos vistas:
- `v_colombia_vs_latam` — compara Colombia con el promedio latinoamericano
- `v_ranking_pib_pc` — ranking de PIB per cápita por año

---

## 🚀 Cómo Ejecutar
```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu contraseña de PostgreSQL

# 4. Ejecutar el ETL
python scripts/extractor.py

# 5. Generar gráficas
python scripts/visualizador.py
```

---

## ✅ Resultados Obtenidos

- 📊 **168 registros** extraídos exitosamente
- 🌍 **7 países** analizados
- 📅 **Período:** 2000 – 2023
- 📁 Datos guardados en `data/worldbank_pib.csv` y `data/worldbank_pib_raw.json`
- 📈 Gráficas guardadas en `data/worldbank_graficas.png`

---

## 🗺️ Fases del Proyecto

| Fase | Carpeta | Descripción | Estado |
|------|---------|-------------|--------|
| 02 | `02-Elt-Proyecto-Api` | ETL completo con World Bank API | ✅ Terminado |
| 03 | `Aplicar-Streamlit-Proyecto` | Dashboard interactivo con Plotly | 🔜 Siguiente |
| 04 | Por definir | PostgreSQL + Docker Compose | 🔜 Pendiente |
| 05 | Por definir | Machine Learning con Jupyter | 🔜 Pendiente |
