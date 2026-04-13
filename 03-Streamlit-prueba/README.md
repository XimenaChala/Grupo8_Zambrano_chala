# 🌤️ ETL Weatherstack - Dashboard de Clima

Proyecto ETL completo que extrae datos de clima desde la API de Weatherstack,
los transforma y los visualiza en dashboards interactivos con Streamlit, con análisis
estadístico de regresión lineal en Jupyter Notebook.

> **Estado:** ✅ En producción | **Despliegue:** Streamlit Cloud + Supabase | **Python:** 3.12

---

## 🚀 Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grupo8zambranochala-3xdpkjdxp8rxvmqcdr2cbj.streamlit.app/)

---

## 🏗️ Arquitectura

```
Tu Máquina (desarrollo)
┌──────────────────┐
│  📁 Código       │──── git push ───▶ GitHub (repositorio público)
│  scripts/        │                         │
│  dashboards      │                         │ Streamlit Cloud
└──────────────────┘                         │ lee el repositorio
                                             ▼
                                  ┌──────────────────────┐
                                  │  Streamlit Cloud      │
                                  │  • Python 3.12        │──▶ URL pública
                                  │  • Lee st.secrets     │    https://xxx
                                  │  • Ejecuta app        │    .streamlit.app
                                  └──────────┬───────────┘
                                             │
                                   SQLAlchemy │ psycopg v3
                                   (pooler)   │ port 6543
                                             ▼
                                  ┌──────────────────────┐
                                  │  Supabase             │
                                  │  • PostgreSQL 15      │
                                  │  • Pooler IPv4        │
                                  │  • SSL requerido      │
                                  └──────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
03-Streamlit-prueba/
│
├── alembic/                    Migraciones de la base de datos
│   └── versions/
│       └── 5869798adfb4_crear_tablas_iniciales.py
│
├── dashboard_interactive.py   ⭐ App principal (Streamlit Cloud)
├── dashboard_app.py            Dashboard básico
├── dashboard_advanced.py       Dashboard con análisis avanzado
│
├── scripts/
│   ├── __init__.py
│   ├── database.py             Conexión a PostgreSQL (nube/local)
│   ├── models.py               Modelos SQLAlchemy
│   ├── demo_data.py            Generador de datos sintéticos
│   ├── transformador.py        Fase Transform del ETL
│   ├── extractor.py            Extrae API → CSV/JSON
│   ├── extractor_db.py         Extrae API → carga directo a DB
│   ├── consultas.py            Queries SQL reutilizables
│   └── test_db.py              Prueba de conexión a la DB
│
├── notebooks/                 ⭐ Análisis estadístico
│   └── regresion_clima.ipynb  EDA + Regresión Lineal Simple y Múltiple
│
├── data/
│   ├── clima.csv               Respaldo de datos
│   ├── clima_raw.json          Datos crudos de la API
│   └── graficas/              ⭐ Gráficas generadas por el notebook
│       ├── eda_distribuciones.png
│       ├── eda_boxplots_ciudad.png
│       ├── eda_correlacion.png
│       ├── eda_scatter.png
│       ├── regresion_simple.png
│       ├── normalidad_simple.png
│       ├── homoc_simple.png
│       ├── coeficientes_multi.png
│       ├── diagnosticos_multi.png
│       └── predicciones_vs_reales.png
│
├── logs/
│   └── etl.log                 Registro de ejecuciones ETL
│
├── .streamlit/
│   ├── config.toml             Tema oscuro y configuración
│   └── secrets.toml            ⚠️ Credenciales (NO se sube a GitHub)
│
├── alembic.ini                 Configuración de migraciones
├── requirements.txt
├── runtime.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/XimenaChala/Grupo8_Zambrano_chala.git
cd Grupo8_Zambrano_chala/03-Streamlit-prueba

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt
```

Crea un archivo `.env` en `03-Streamlit-prueba/`:

```env
API_KEY=tu_api_key_de_weatherstack
WEATHERSTACK_BASE_URL=http://api.weatherstack.com
CIUDADES=Bogota,Medellin,Cali,Barranquilla,Cartagena
DATABASE_URL=postgresql+psycopg://postgres.tu_project_ref:tu_password@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require
DB_HOST=aws-1-us-east-1.pooler.supabase.com
DB_PORT=6543
DB_USER=postgres.tu_project_ref
DB_PASSWORD=tu_password
DB_NAME=postgres
```

---

## ▶️ Uso

```bash
# Extraer datos de la API → guarda en CSV/JSON
python scripts/extractor.py

# Extraer y cargar directo a PostgreSQL (Supabase)
python scripts/extractor_db.py

# Probar conexión a la base de datos
python scripts/test_db.py

# Lanzar el dashboard localmente
streamlit run dashboard_interactive.py


Se abre en: `http://localhost:8501`

---

## ☁️ Despliegue en Streamlit Cloud + Supabase

### 1. Configurar Supabase
1. Crear proyecto en [supabase.com](https://supabase.com)
2. Crear las 3 tablas via SQL Editor (`ciudades`, `registros_clima`, `metricas_etl`)
3. Obtener credenciales del **Transaction Pooler** (puerto 6543)

### 2. Cargar datos
```bash
python scripts/extractor_db.py
```

### 3. Subir a GitHub
```bash
git add .
git commit -m "feat: ETL pipeline"
git push origin main
```

### 4. Desplegar en Streamlit Cloud
1. En [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Selecciona: `03-Streamlit-prueba/dashboard_interactive.py`
3. En **Advanced settings → Secrets** agrega:

```toml
DATABASE_URL = "postgresql+psycopg://postgres.tu_project_ref:tu_password@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
DB_HOST = "aws-1-us-east-1.pooler.supabase.com"
DB_PORT = "6543"
DB_USER = "postgres.tu_project_ref"
DB_PASSWORD = "tu_password"
DB_NAME = "postgres"
```

---

## 🗄️ Migraciones con Alembic

```bash
# Inicializar Alembic
alembic init alembic

# Generar migración automática
alembic revision --autogenerate -m "crear tablas iniciales"

# Aplicar migración
alembic upgrade head
```

---

## 📓 Análisis Estadístico — Jupyter Notebook

El notebook `notebooks/regresion_clima.ipynb` implementa 23 celdas con:

### EDA (Análisis Exploratorio de Datos)
- Estadísticas descriptivas de las 4 variables climáticas
- Histogramas de distribución
- Boxplots por ciudad
- Matriz de correlación
- Scatter plots bivariados

### Regresión Lineal Simple
- Variable objetivo: `sensacion_termica`
- Feature: `temperatura`
- **R² ≈ 0.965 | RMSE ≈ 0.82°C**

### Regresión Lineal Múltiple
- Features: `temperatura`, `humedad`, `velocidad_viento`
- **R² ≈ 0.972 | RMSE ≈ 0.75°C**

### Diagnósticos Estadísticos
| Supuesto | Test | Visual |
|---|---|---|
| Normalidad | Shapiro-Wilk | Q-Q Plot |
| Homocedasticidad | Breusch-Pagan | Residuos vs Ajustados |
| Multicolinealidad | VIF | Gráfica de coeficientes |

```bash
# Lanzar Jupyter Notebook (independiente de Streamlit)
source venv/bin/activate
jupyter notebook
# Navegar a notebooks/ → regresion_clima.ipynb → Kernel > Restart & Run All
```

---

## 📊 Dashboards Disponibles

| Archivo | Descripción |
|---|---|
| `dashboard_interactive.py` | ⭐ Principal — filtros, KPIs, gráficas, descarga CSV |
| `dashboard_app.py` | Vista rápida y sencilla de los datos |
| `dashboard_advanced.py` | Análisis histórico + métricas de ejecución ETL |

---

## 🛠️ Tecnologías

| Categoría | Herramientas |
|---|---|
| Lenguaje | Python 3.12 |
| Dashboard | Streamlit, Plotly |
| Datos | Pandas, NumPy |
| Base de datos | Supabase (PostgreSQL 15), SQLAlchemy, psycopg v3 |
| Migraciones | Alembic |
| ETL | Requests, python-dotenv |
| Análisis ML | scikit-learn, statsmodels, scipy, seaborn |
| Notebooks | Jupyter Notebook |
| Control de versiones | Git, GitHub |
| Despliegue | Streamlit Cloud |

---

## 🔐 Seguridad

- `.env` y `secrets.toml` excluidos del repositorio via `.gitignore`
- Credenciales solo en Streamlit Cloud Secrets (producción) y `.env` (local)
- Conexión con `sslmode=require` obligatorio
- Connection Pooler IPv4 para compatibilidad con Streamlit Cloud

---

## 👩‍💻 Autores

**Grupo 8** — Ximena del pilar zambrano chala 
Ingeniería de Sistemas — CORHUILA

---

## 📝 Licencia  

Este proyecto está bajo licencia MIT.

---

*Última actualización: Abril 2026*