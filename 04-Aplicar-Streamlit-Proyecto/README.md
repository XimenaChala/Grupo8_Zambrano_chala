<div align="center">

# 🌎 World Bank Dashboard — Análisis PIB Colombia

### 👩‍💻 Grupo 8 — Ximena del Pilar Zambrano Chala
### 📧 xdzambrano-2022b@corhuila.edu.co
### 🏫 CORHUILA — Ingeniería de Sistemas — Minería de Datos

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grupo8zambranochala-sccr9ysvtqykwtktandvgj.streamlit.app/)

</div>

---

## 📌 Objetivo del Proyecto

Construir un sistema completo de ingeniería de datos que extrae automáticamente indicadores económicos del **World Bank API**, los procesa, los almacena en PostgreSQL y los presenta en un dashboard interactivo con modelos de Machine Learning para predecir el PIB de Colombia.

---

## ❓ Pregunta de Investigación

> ¿Cómo ha evolucionado el crecimiento económico de Colombia entre 2000 y 2023 en comparación con América Latina, y qué factores predicen mejor su PIB futuro?

---

## 📊 Descripción de los Datos

| Característica | Detalle |
|---|---|
| **Fuente** | World Bank Open Data API (gratuita, sin API key) |
| **Países** | Colombia, USA, Brasil, México, Argentina, Chile, Perú |
| **Período** | 2000 – 2023 (24 años) |
| **Registros** | 168 registros limpios |
| **Indicadores** | PIB, crecimiento PIB, PIB per cápita, inflación, desempleo, exportaciones, importaciones |

---

## 🎯 Alcance del Proyecto

- ✅ Extracción automática de datos desde la API del Banco Mundial
- ✅ Transformación: limpieza de nulos, normalización y enriquecimiento
- ✅ Carga en PostgreSQL con fallback automático a CSV
- ✅ Dashboard interactivo con 4 secciones y filtros dinámicos
- ✅ 3 modelos de Machine Learning implementados y evaluados
- ✅ Presentación de resultados con métricas de evaluación

---

## 🛠️ Tecnologías y Herramientas

| Herramienta | Uso |
|---|---|
| 🐍 Python 3.11 | Lenguaje principal |
| 🌐 World Bank API | Fuente de datos |
| 🐼 Pandas | Transformación y limpieza ETL |
| 📊 Streamlit | Dashboard web interactivo |
| 📈 Plotly | Visualizaciones interactivas |
| 🤖 Scikit-learn | Modelos de Machine Learning |
| 🐘 PostgreSQL | Base de datos relacional |
| 💻 VS Code | Entorno de desarrollo |
| 🐧 Ubuntu (Linux) | Sistema operativo |

---

## 📁 Estructura del Proyecto

```
04-Aplicar-Streamlit-Proyecto/
├── dashboard_interactive.py  ⭐ App principal (4 secciones)
├── dashboard_app.py          Dashboard básico
├── dashboard_advanced.py     Dashboard avanzado
├── scripts/
│   ├── database.py           Conexión PostgreSQL + fallback CSV
│   ├── models.py             Tablas SQLAlchemy ORM
│   ├── extractor.py          Extrae API → CSV
│   ├── extractor_db.py       Extrae API → PostgreSQL
│   ├── consultas.py          Queries reutilizables
│   └── test_db.py            Tests de conexión
├── notebooks/
│   └── analisis_ml.ipynb     3 modelos de Machine Learning
├── data/
│   └── worldbank_pib.csv     Datos generados por el ETL
├── logs/
│   └── etl.log               Registro de ejecución
├── requirements.txt
├── .env.example
└── README.md
```

---

## 💡 Solución Propuesta — Arquitectura ETL

```
World Bank API  →  extractor.py  →  PostgreSQL + CSV  →  Streamlit Dashboard  →  ML Notebook
     🌐                ⚙️                🐘 📄                    📊                    🤖
  (Extracción)    (Transformación)       (Carga)            (Visualización)        (Predicción)
```

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/XimenaChala/Grupo8_Zambrano_chala.git
cd Grupo8_Zambrano_chala/04-Aplicar-Streamlit-Proyecto
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con las credenciales de PostgreSQL
```

### 4. Extraer datos y cargar a PostgreSQL
```bash
python scripts/extractor_db.py
```

### 5. Ejecutar el dashboard
```bash
streamlit run dashboard_interactive.py
# Abre: http://localhost:8501
```

---

## 📊 Secciones del Dashboard

| Sección | Descripción |
|---------|-------------|
| 📊 Resumen General | KPIs Colombia, evolución PIB total y crecimiento por país |
| 🇨🇴 Colombia Detalle | PIB, inflación vs desempleo, tabla descargable en CSV |
| 🌎 Comparativa Regional | Colombia vs promedio LATAM, ranking PIB per cápita |
| ⚖️ Balanza Comercial | Exportaciones, importaciones y balance comercial |

---

## 🗄️ Base de Datos

El dashboard carga datos en orden de prioridad:

1. **🐘 PostgreSQL** — si hay conexión disponible
2. **📄 CSV fallback** — si no hay BD usa `data/worldbank_pib.csv`

---

## 🤖 Machine Learning

| # | Modelo | Objetivo | Métricas |
|---|--------|----------|----------|
| 1 | Regresión Lineal | Predecir PIB per cápita Colombia 2024–2027 | R² = 0.92, MAE ~$450 |
| 2 | Random Forest | Variables que más influyen en el crecimiento PIB | R² = 0.78, RMSE ~1.8% |
| 3 | K-Means Clustering | Agrupar países por similitud económica | k = 3 clusters |

---

## ✅ Resultados Obtenidos

- ✅ Pipeline ETL completo: API → transformación → PostgreSQL → dashboard
- ✅ Dashboard con 4 secciones interactivas y descarga de datos en CSV
- ✅ 168 registros procesados de 7 países durante 24 años
- ✅ 3 modelos de ML implementados con métricas de evaluación
- ✅ Conexión dual PostgreSQL + CSV para máxima disponibilidad

---

## 🗺️ Fases del Proyecto

| Fase | Carpeta | Descripción | Estado |
|------|---------|-------------|--------|
| 02 | `02-Elt-Proyecto-Api` | ETL completo World Bank API | ✅ Terminado |
| 04 | `04-Aplicar-Streamlit-Proyecto` | Dashboard + ML | ✅ Terminado |

---

## 🔗 Fuente de Datos

- **API:** https://api.worldbank.org/v2/
- **Sin API Key** — completamente gratuita
- **Documentación:** https://datahelpdesk.worldbank.org/knowledgebase/articles/898581