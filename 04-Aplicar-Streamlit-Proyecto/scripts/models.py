"""
models.py - Definición de tablas PostgreSQL con SQLAlchemy ORM
"""

from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class IndicadorPIB(Base):
    __tablename__ = "indicadores_pib"

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    pais_codigo             = Column(String(3),   nullable=False)
    pais_nombre             = Column(String(100))
    anio                    = Column(Integer,      nullable=False)
    pib_usd                 = Column(Numeric(25, 4))
    crecimiento_pib_pct     = Column(Numeric(10, 4))
    pib_per_capita_usd      = Column(Numeric(15, 4))
    crecimiento_pib_pc_pct  = Column(Numeric(10, 4))
    inflacion_pct           = Column(Numeric(10, 4))
    desempleo_pct           = Column(Numeric(10, 4))
    exportaciones_pct_pib   = Column(Numeric(10, 4))
    importaciones_pct_pib   = Column(Numeric(10, 4))
    balanza_comercial_pct   = Column(Numeric(10, 4))
    region                  = Column(String(50))
    es_colombia             = Column(Boolean, default=False)
    fecha_extraccion        = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint("pais_codigo", "anio", name="uq_pais_anio"),
    )


class Pais(Base):
    __tablename__ = "paises"

    codigo   = Column(String(3),   primary_key=True)
    nombre   = Column(String(100))
    region   = Column(String(50))
    es_foco  = Column(Boolean, default=False)


def crear_tablas(engine):
    Base.metadata.create_all(engine)
    print("✅ Tablas creadas exitosamente.")
