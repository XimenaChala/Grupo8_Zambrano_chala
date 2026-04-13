"""
models.py — Modelos SQLAlchemy alineados con las tablas creadas en Supabase.
"""
from sqlalchemy import (
    Column, Integer, String, Float, Double,
    DateTime, Boolean, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Ciudad(Base):
    __tablename__ = "ciudades"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    nombre         = Column(String(100), unique=True, nullable=False)
    pais           = Column(String(100), nullable=False)
    latitud        = Column(Double)
    longitud       = Column(Double)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    activa         = Column(Boolean, default=True)

    __table_args__ = (
        Index("ix_ciudades_nombre", "nombre"),
    )


class RegistroClima(Base):
    __tablename__ = "registros_clima"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    ciudad_id         = Column(Integer, ForeignKey("ciudades.id"), nullable=False)
    temperatura       = Column(Double, nullable=False)
    sensacion_termica = Column(Double)
    humedad           = Column(Double, nullable=False)
    velocidad_viento  = Column(Double, nullable=False)
    descripcion       = Column(String(255), nullable=False)
    codigo_tiempo     = Column(Integer)
    fecha_extraccion  = Column(DateTime, default=datetime.utcnow)
    fecha_creacion    = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_registros_clima_ciudad_id", "ciudad_id"),
        Index("ix_registros_clima_fecha_extraccion", "fecha_extraccion"),
        Index("idx_ciudad_fecha", "ciudad_id", "fecha_extraccion"),
    )


class MetricasETL(Base):
    __tablename__ = "metricas_etl"

    id                        = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ejecucion           = Column(DateTime, default=datetime.utcnow)
    registros_extraidos       = Column(Integer, nullable=False)
    registros_guardados       = Column(Integer, nullable=False)
    registros_fallidos        = Column(Integer, default=0)
    tiempo_ejecucion_segundos = Column(Float, nullable=False)
    estado                    = Column(String(50), nullable=False)
    mensaje                   = Column(String(500))

    __table_args__ = (
        Index("ix_metricas_etl_fecha", "fecha_ejecucion"),
    )