-- ============================================================
-- Base de datos: worldbank_db
-- Proyecto: ETL World Bank - PIB y Crecimiento Económico
-- ============================================================

-- 1. Crear la base de datos (ejecutar como superusuario)
-- CREATE DATABASE worldbank_db;

-- 2. Conectarse a worldbank_db antes de ejecutar lo siguiente:
-- \c worldbank_db

-- ── Tabla principal de indicadores ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS indicadores_pib (
    id                      SERIAL PRIMARY KEY,
    pais_codigo             VARCHAR(3)    NOT NULL,
    pais_nombre             VARCHAR(100),
    anio                    INTEGER       NOT NULL,
    pib_usd                 NUMERIC(25,4),          -- PIB en USD corrientes
    crecimiento_pib_pct     NUMERIC(10,4),          -- Crecimiento PIB (%)
    pib_per_capita_usd      NUMERIC(15,4),          -- PIB per cápita USD
    crecimiento_pib_pc_pct  NUMERIC(10,4),          -- Crecimiento PIB per cápita (%)
    inflacion_pct           NUMERIC(10,4),          -- Inflación (%)
    desempleo_pct           NUMERIC(10,4),          -- Desempleo (%)
    exportaciones_pct_pib   NUMERIC(10,4),          -- Exportaciones % PIB
    importaciones_pct_pib   NUMERIC(10,4),          -- Importaciones % PIB
    region                  VARCHAR(50),
    es_colombia             BOOLEAN DEFAULT FALSE,
    fecha_extraccion        TIMESTAMP DEFAULT NOW(),
    CONSTRAINT uq_pais_anio UNIQUE (pais_codigo, anio)
);

-- ── Tabla de países (catálogo) ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS paises (
    codigo      VARCHAR(3)  PRIMARY KEY,
    nombre      VARCHAR(100),
    region      VARCHAR(50),
    es_foco     BOOLEAN DEFAULT FALSE   -- TRUE = Colombia (país principal)
);

INSERT INTO paises VALUES
    ('CO', 'Colombia',       'América Latina', TRUE),
    ('US', 'United States',  'Referencia',     FALSE),
    ('BR', 'Brazil',         'América Latina', FALSE),
    ('MX', 'Mexico',         'América Latina', FALSE),
    ('AR', 'Argentina',      'América Latina', FALSE),
    ('CL', 'Chile',          'América Latina', FALSE),
    ('PE', 'Peru',           'América Latina', FALSE)
ON CONFLICT (codigo) DO NOTHING;

-- ── Índices para mejorar rendimiento ─────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_pib_pais   ON indicadores_pib (pais_codigo);
CREATE INDEX IF NOT EXISTS idx_pib_anio   ON indicadores_pib (anio);
CREATE INDEX IF NOT EXISTS idx_pib_region ON indicadores_pib (region);

-- ── Vista útil: Comparativa Colombia vs América Latina ────────────────────────
CREATE OR REPLACE VIEW v_colombia_vs_latam AS
SELECT
    anio,
    MAX(CASE WHEN pais_codigo = 'CO' THEN crecimiento_pib_pct END)  AS colombia_crecimiento,
    AVG(CASE WHEN region = 'América Latina' THEN crecimiento_pib_pct END) AS latam_promedio,
    MAX(CASE WHEN pais_codigo = 'CO' THEN pib_per_capita_usd END)   AS colombia_pib_pc,
    MAX(CASE WHEN pais_codigo = 'CO' THEN inflacion_pct END)        AS colombia_inflacion,
    MAX(CASE WHEN pais_codigo = 'CO' THEN desempleo_pct END)        AS colombia_desempleo
FROM indicadores_pib
GROUP BY anio
ORDER BY anio;

-- ── Vista: Ranking PIB per cápita por año ─────────────────────────────────────
CREATE OR REPLACE VIEW v_ranking_pib_pc AS
SELECT
    anio,
    pais_codigo,
    pais_nombre,
    pib_per_capita_usd,
    RANK() OVER (PARTITION BY anio ORDER BY pib_per_capita_usd DESC) AS ranking
FROM indicadores_pib
WHERE pib_per_capita_usd IS NOT NULL;

-- ── Consultas de verificación ─────────────────────────────────────────────────
-- SELECT COUNT(*) FROM indicadores_pib;
-- SELECT * FROM v_colombia_vs_latam LIMIT 10;
-- SELECT * FROM v_ranking_pib_pc WHERE anio = 2022 ORDER BY ranking;
