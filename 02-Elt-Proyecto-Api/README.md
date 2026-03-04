# 📦 02 - ETL Proyecto API – World Bank PIB

Pipeline ETL que extrae indicadores económicos de la **World Bank API** para Colombia y países comparados.

## 👥 Grupo 8 – Zambrano & Chala

## 📁 Estructura
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
│   ├── extractor.py      ← EXTRACT: llama la API y guarda datos
│   ├── transformador.py  ← TRANSFORM: limpia y enriquece el DataFrame
│   └── visualizador.py   ← Genera gráficas con matplotlib
└── logs/
    └── etl.log
```

## 🚀 Cómo ejecutar
```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Ejecutar ETL
python scripts/extractor.py

# 5. Generar gráficas
python scripts/visualizador.py
```

## 🌐 API Fuente

- **URL:** https://api.worldbank.org/v2/
- **Sin API Key** — completamente gratuita
- **Docs:** https://data.worldbank.org/developers

## 📊 Indicadores extraídos

| Indicador | Descripción |
|-----------|-------------|
| NY.GDP.MKTP.CD | PIB total USD |
| NY.GDP.MKTP.KD.ZG | Crecimiento PIB (%) |
| NY.GDP.PCAP.CD | PIB per cápita USD |
| NY.GDP.PCAP.KD.ZG | Crecimiento PIB per cápita (%) |
| FP.CPI.TOTL.ZG | Inflación (%) |
| SL.UEM.TOTL.ZS | Desempleo (%) |
| NE.EXP.GNFS.ZS | Exportaciones % PIB |
| NE.IMP.GNFS.ZS | Importaciones % PIB |

## 🌍 Países analizados

| Código | País | Rol |
|--------|------|-----|
| CO | Colombia | **País foco** |
| US | United States | Referencia |
| BR | Brazil | América Latina |
| MX | Mexico | América Latina |
| AR | Argentina | América Latina |
| CL | Chile | América Latina |
| PE | Peru | América Latina |

## ✅ Resultados

- **168 registros** extraídos exitosamente
- **7 países** analizados
- **Período:** 2000 – 2023
- Datos guardados en `data/worldbank_pib.csv` y `data/worldbank_pib_raw.json`
