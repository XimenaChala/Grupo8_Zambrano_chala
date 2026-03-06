
# 📊 04 - Aplicar Streamlit Proyecto – World Bank Dashboard

Dashboard interactivo con análisis de indicadores económicos del World Bank, modelos de Machine Learning y containerización con Docker.

## 👥 Grupo 8 – Zambrano & Chala

---
## 🚀 Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grupo8zambranochala-sccr9ysvtqykwtktandvgj.streamlit.app/)


## 🔍 ¿Qué es este proyecto?

Una aplicación web interactiva construida con **Streamlit** que consume los datos extraídos por el ETL (proyecto 02) y los presenta en visualizaciones dinámicas. Permite comparar el desempeño económico de Colombia frente a otros países de América Latina entre 2000 y 2023.

---

## 📁 Estructura
```
04-Aplicar-Streamlit-Proyecto/
├── dashboard_interactive.py  ⭐ App principal (4 secciones)
├── dashboard_app.py          Dashboard básico
├── dashboard_advanced.py     Dashboard avanzado
├── scripts/
│   ├── database.py           Conexión PostgreSQL / fallback CSV
│   ├── models.py             Tablas SQLAlchemy ORM
│   ├── extractor.py          Extrae API → CSV
│   ├── extractor_db.py       Extrae API → PostgreSQL
│   ├── consultas.py          Queries reutilizables
│   └── test_db.py            Tests de conexión
├── notebooks/
│   └── analisis_ml.ipynb     3 modelos de Machine Learning
├── data/                     CSV generado automáticamente
├── logs/
│   └── etl.log               Registro de ejecución
├── docker-compose.yml        PostgreSQL + Streamlit en Docker
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Cómo Ejecutar
```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Ejecutar dashboard principal
streamlit run dashboard_interactive.py
# Abre: http://localhost:8501
```

---
## ☁️ Despliegue en Streamlit Cloud

1. Sube el proyecto a GitHub
2. En [Streamlit Cloud](https://streamlit.io/cloud) → **New app**
3. Selecciona el archivo principal: `04-Aplicar-Streamlit-Proyecto/dashboard_interactive.py`


## 🐳 Con Docker
```bash
docker-compose up --build
# Dashboard en: http://localhost:8501
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

## 🗄️ Fuente de Datos

El dashboard carga datos de dos fuentes en orden de prioridad:

1. **PostgreSQL** — si hay conexión disponible lee directo de la BD
2. **CSV fallback** — si no hay BD usa `data/worldbank_pib.csv` generado por el ETL

---

## 🤖 Machine Learning (notebooks/analisis_ml.ipynb)

| # | Modelo | Objetivo | Métricas |
|---|--------|----------|----------|
| 1 | Regresión Lineal | Predecir PIB per cápita Colombia 2024-2027 | R², MAE |
| 2 | Random Forest | Identificar variables que más influyen en el crecimiento PIB | R², RMSE |
| 3 | K-Means Clustering | Agrupar países por similitud económica | k=3 clusters |

---

## 📦 Scripts

| Script | Descripción |
|--------|-------------|
| `database.py` | Conecta a PostgreSQL, si falla usa CSV automáticamente |
| `models.py` | Define las tablas con SQLAlchemy ORM |
| `extractor.py` | Extrae datos del World Bank API y guarda en CSV |
| `extractor_db.py` | Extrae datos y carga directo a PostgreSQL |
| `consultas.py` | Funciones reutilizables: rankings, comparativas, balanza |
| `test_db.py` | Verifica conexión y calidad de los datos |

---

## ✅ Resultados

- ✅ Dashboard con **4 secciones** interactivas
- ✅ **168 registros** de 7 países (2000-2023)
- ✅ Conexión dual: PostgreSQL + CSV fallback
- ✅ **3 modelos ML** implementados en Jupyter
- ✅ Containerizado con Docker Compose

---

## 🗺️ Fases del Proyecto

| Fase | Carpeta | Descripción | Estado |
|------|---------|-------------|--------|
| 02 | `02-Elt-Proyecto-Api` | ETL completo World Bank API | ✅ Terminado |
| 04 | `04-Aplicar-Streamlit-Proyecto` | Dashboard + ML + Docker | ✅ Terminado |

---

## 🔗 Fuente de Datos

- **API:** https://api.worldbank.org/v2/
- **Sin API Key** — completamente gratuita
- **Período:** 2000 – 2023
- **Países:** CO, US, BR, MX, AR, CL, PE

<div align="center">

# 🔎 Minería de Datos

### 👩‍💻 Grupo 8 — Ximena del Pilar Zambrano Chala

</div>

---

## 📌 Objetivo del Proyecto
> *(Aquí explicarás qué busca resolver el proyecto, propósito principal y resultados esperados.)*

---

## 📊 Descripción de los Datos
✔ Fuente de los datos  
✔ Tipo de datos  
✔ Variables principales  
✔ Características del dataset  

*(Aquí agregarás la información detallada.)*

---

## 🎯 Alcance del Proyecto
- ✔ Qué incluye el proyecto  
- ✔ Qué procesos se realizan  
- ✔ Limitaciones o exclusiones  

*(Aquí escribirás el alcance.)*

---

## 🛠️ Tecnologías y Herramientas

| Herramienta | Uso |
|---|---|
| 💻 VS Code | Desarrollo del proyecto |
| 🐍 Python | Procesamiento y análisis |
| 🐧 WSL | Entorno Linux |
| 🐳 Docker | Contenedores |
| 📈 Streamlit | Visualización |
| 🤖 Scikit-learn | Machine Learning |

---

## 💡 Solución Propuesta
*(Explicación del enfoque, modelo, proceso o metodología utilizada.)*

---

## 📂 Estructura del Proyecto


*(Luego la ajustamos a tu estructura real.)*

---

## 🚀 Instalación y Uso

### Clonar el repositorio
```bash
git clone <https://github.com/XimenaChala/Grupo1_Zambrano_chala.git>
```

## 👩‍💻 Autor

### Ximena del Pilar Zambrano Chala
### 📧 xdzambrano-2022b@corhuila.edu.co
>>>>>>> f07a00e6bf132fb47e3a5a389f5d73ab75cac48b
