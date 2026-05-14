<div align="center">

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>

# 🌎 World Bank Dashboard
### Análisis de Indicadores Económicos de América Latina (2000–2023)

**Minería de Datos · Séptimo Semestre · Grupo 8**
👩‍💻 Ximena del Pilar Zambrano Chala

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grupo8zambranochala-sccr9ysvtqykwtktandvgj.streamlit.app/)

</div>

---

## 📌 Objetivo del Proyecto

Desarrollar un **dashboard interactivo** que integre un proceso ETL desde la API pública del Banco Mundial, una base de datos PostgreSQL y modelos de Machine Learning, para facilitar el **análisis comparativo de indicadores económicos** de Colombia frente a otros países de América Latina entre 2000 y 2023.

El proyecto permite identificar tendencias, predecir comportamientos futuros del PIB y agrupar países por similitud económica, todo desde una interfaz web accesible sin instalación.

---

## 📊 Descripción de los Datos

| Atributo | Detalle |
|---|---|
| 🌐 **Fuente** | [API pública del Banco Mundial](https://api.worldbank.org/v2/) — sin API Key |
| 📅 **Período** | 2000 – 2023 |
| 🗂️ **Registros** | 168 registros |
| 🌍 **Países** | Colombia (CO), Brasil (BR), México (MX), Argentina (AR), Chile (CL), Perú (PE), Estados Unidos (US) |
| 📈 **Variables principales** | PIB total, PIB per cápita, Inflación, Desempleo, Exportaciones, Importaciones, Balanza Comercial |
| 💾 **Almacenamiento** | PostgreSQL (primario) + CSV fallback automático |

---

## 🎯 Alcance del Proyecto

**✔ Incluye:**
- Pipeline ETL completo: extracción desde API → transformación → carga en PostgreSQL y CSV
- Dashboard interactivo con 4 secciones de análisis
- 3 modelos de Machine Learning entrenados y evaluados
- Containerización con Docker Compose
- Despliegue en producción vía Streamlit Cloud

**✔ Procesos realizados:**
- Extracción automatizada de datos desde la API del Banco Mundial
- Almacenamiento relacional con SQLAlchemy ORM
- Visualización comparativa por país, año e indicador
- Predicción del PIB per cápita de Colombia hasta 2027
- Clustering de países por similitud económica

**⚠️ Limitaciones:**
- Datos disponibles únicamente hasta 2023 (límite de la API pública)
- Los modelos ML fueron entrenados con datos históricos; las predicciones son estimaciones
- Requiere conexión a internet para el despliegue en la nube

---

## 🛠️ Tecnologías y Herramientas

| Herramienta | Versión | Uso |
|---|---|---|
| 🐍 Python | 3.11 | Lenguaje principal |
| 📈 Streamlit | Latest | Dashboard interactivo y despliegue |
| 🐘 PostgreSQL | 15 | Base de datos relacional |
| 🔗 SQLAlchemy | Latest | ORM para modelado de tablas |
| 🤖 Scikit-learn | Latest | Modelos de Machine Learning |
| 🐼 Pandas | Latest | Procesamiento y análisis de datos |
| 📊 Plotly | Latest | Visualizaciones interactivas |
| 🐳 Docker | Latest | Containerización de la aplicación |
| 💻 VS Code | - | Entorno de desarrollo |
| 🐧 WSL | Ubuntu | Entorno Linux en Windows |

---

## 💡 Solución Propuesta

El proyecto se estructura en **cuatro fases** interconectadas:

```
API Banco Mundial
       ↓
  [ETL Pipeline]  →  extractor.py / extractor_db.py
       ↓
  PostgreSQL DB   →  SQLAlchemy ORM (models.py)
  + CSV fallback  →  Automático si no hay BD disponible
       ↓
  Dashboard       →  dashboard_interactive.py (4 secciones)
       ↓
  ML Models       →  analisis_ml.ipynb
  ┣ Regresión Lineal   → Predice PIB per cápita 2024-2027
  ┣ Random Forest      → Variables más influyentes en el PIB
  └ K-Means Clustering → Agrupa países por similitud económica
```

### 📊 Secciones del Dashboard

| # | Sección | Descripción |
|---|---|---|
| 1 | 📊 Resumen General | KPIs Colombia, evolución PIB total y crecimiento por país |
| 2 | 🇨🇴 Colombia Detalle | PIB, inflación vs desempleo, tabla descargable en CSV |
| 3 | 🌎 Comparativa Regional | Colombia vs promedio LATAM, ranking PIB per cápita |
| 4 | ⚖️ Balanza Comercial | Exportaciones, importaciones y balance comercial |

### 🤖 Modelos de Machine Learning

| Modelo | Objetivo | Métricas |
|---|---|---|
| Regresión Lineal | Predecir PIB per cápita Colombia 2024–2027 | R², MAE |
| Random Forest | Identificar variables clave del crecimiento económico | R², RMSE |
| K-Means Clustering | Agrupar países por similitud económica | k=3 clusters |

---

## 📂 Estructura del Proyecto

```
Grupo8_Zambrano_Chala/
│
├── 02-Elt-Proyecto-Api/              # Fase ETL
│   ├── extractor.py                  # Extrae API → CSV
│   └── extractor_db.py               # Extrae API → PostgreSQL
│
├── 04-Aplicar-Streamlit-Proyecto/    # Fase Dashboard
│   ├── dashboard_interactive.py  ⭐  # App principal (4 secciones)
│   ├── dashboard_app.py              # Dashboard básico
│   ├── dashboard_advanced.py         # Dashboard avanzado
│   ├── scripts/
│   │   ├── database.py               # Conexión PostgreSQL / fallback CSV
│   │   ├── models.py                 # Tablas SQLAlchemy ORM
│   │   ├── consultas.py              # Queries reutilizables
│   │   └── test_db.py                # Tests de conexión
│   ├── notebooks/
│   │   └── analisis_ml.ipynb         # 3 modelos de Machine Learning
│   ├── data/
│   │   └── worldbank_pib.csv         # CSV generado por el ETL
│   ├── logs/
│   │   └── etl.log                   # Registro de ejecución
│   ├── docker-compose.yml            # PostgreSQL + Streamlit en Docker
│   ├── .env.example
│   └── requirements.txt
│
└── README.md
```

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/XimenaChala/Grupo1_Zambrano_chala.git
cd Grupo1_Zambrano_chala
```

### 2. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL
```

### 4. Ejecutar el dashboard

```bash
cd 04-Aplicar-Streamlit-Proyecto
streamlit run dashboard_interactive.py
# Abre: http://localhost:8501
```

### 🐳 Alternativa con Docker

```bash
docker-compose up --build
# Dashboard en: http://localhost:8501
```

---

## ✅ Resultados Obtenidos

- ✅ **168 registros** procesados de 7 países (2000–2023)
- ✅ Dashboard con **4 secciones** interactivas en producción
- ✅ **3 modelos ML** implementados y evaluados en Jupyter
- ✅ Conexión dual PostgreSQL + CSV fallback funcional
- ✅ Containerizado con **Docker Compose**
- ✅ Desplegado en **Streamlit Cloud** (acceso público sin instalación)

---

## 📚 Bibliografía

- World Bank Open Data. (2024). *World Development Indicators*. https://data.worldbank.org/
- Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io/
- McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

---

## 👩‍💻 Autora

**Ximena del Pilar Zambrano Chala**
📧 xdzambrano-2022b@corhuila.edu.co
🏫 CORHUILA · Facultad de Ingeniería · Ingeniería de Sistemas · Séptimo Semestre

---

<div align="center">
<sub>Proyecto de Aula · Minería de Datos · 2025 · CORHUILA</sub>
</div>