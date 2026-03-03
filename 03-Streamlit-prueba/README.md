# 🌤️ ETL Weatherstack - Dashboard de Clima

Proyecto ETL completo que extrae datos de clima desde la API de Weatherstack,
los transforma y los visualiza en dashboards interactivos con Streamlit.

> **Estado:** ✅ En producción | **Despliegue:** Streamlit Cloud | **Python:** 3.12

---

## 🚀 Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grupo8zambranochala-3xdpkjdxp8rxvmqcdr2cbj.streamlit.app/)

---

## 📁 Estructura del Proyecto

```
03-Streamlit-prueba/
│
├── dashboard_interactive.py   ⭐ App principal (Streamlit Cloud)
├── dashboard_app.py            Dashboard básico
├── dashboard_advanced.py       Dashboard con análisis avanzado
│
├── scripts/
│   ├── __init__.py
│   ├── database.py             Conexión a PostgreSQL (nube/local)
│   ├── models.py               Modelos SQLAlchemy
│   ├── extractor.py            Extrae API → CSV/JSON
│   ├── extractor_db.py         Extrae API → carga directo a DB
│   ├── consultas.py            Queries SQL reutilizables
│   └── test_db.py              Prueba de conexión a la DB
│
├── data/
│   ├── clima.csv               Respaldo de datos
│   └── clima_raw.json          Datos crudos de la API
│
├── logs/
│   └── etl.log                 Registro de ejecuciones ETL
│
├── .streamlit/
│   ├── config.toml             Tema oscuro y configuración
│   └── secrets.toml            ⚠️ Credenciales (NO se sube a GitHub)
│
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
DATABASE_URL=postgresql+psycopg://etl_user:etl_pass@localhost:5433/weatherstack_dw
```

---

## ▶️ Uso

```bash
# Extraer datos de la API → guarda en CSV/JSON
python scripts/extractor.py

# Extraer y cargar directo a PostgreSQL
python scripts/extractor_db.py

# Probar conexión a la base de datos
python scripts/test_db.py

# Lanzar el dashboard localmente
streamlit run dashboard_interactive.py
```

Se abre en: `http://localhost:8501`

---

## ☁️ Despliegue en Streamlit Cloud

1. Sube el proyecto a GitHub
2. En [Streamlit Cloud](https://streamlit.io/cloud) → **New app**
3. Selecciona el archivo principal: `03-Streamlit-prueba/dashboard_interactive.py`
4. En **Settings → Secrets** agrega:

```toml
DATABASE_URL = "postgresql+psycopg://usuario:password@host:puerto/dbname"
```

> Si no hay base de datos configurada, el dashboard usa automáticamente
> `data/clima.csv` como respaldo.

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
| Base de datos | PostgreSQL, SQLAlchemy, psycopg v3 |
| ETL | Requests, python-dotenv |
| Control de versiones | Git, GitHub |
| Despliegue | Streamlit Cloud |

---

## 👩‍💻 Autores

**Grupo 8** — Zambrano & Chala  
Ingeniería de Sistemas — CORHUILA  

---

## 📝 Licencia

Este proyecto está bajo licencia MIT.

---

*Última actualización: Marzo 2026*
