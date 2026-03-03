from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Ciudad(Base):
    __tablename__ = 'ciudades'
    id     = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    pais   = Column(String)

class RegistroClima(Base):
    __tablename__ = 'clima'
    id                = Column(Integer, primary_key=True)
    ciudad_id         = Column(Integer, ForeignKey('ciudades.id'))
    ciudad            = Column(String)
    pais              = Column(String)
    latitud           = Column(Float)
    longitud          = Column(Float)
    temperatura       = Column(Float)
    sensacion_termica = Column(Float)
    humedad           = Column(Integer)
    velocidad_viento  = Column(Float)
    descripcion       = Column(String)
    fecha_extraccion  = Column(DateTime)
    codigo_tiempo     = Column(Integer)

class MetricasETL(Base):
    __tablename__ = 'metricas_etl'
    id                        = Column(Integer, primary_key=True)
    fecha_ejecucion           = Column(DateTime, default=datetime.utcnow)
    estado                    = Column(String)
    registros_extraidos       = Column(Integer, default=0)
    registros_guardados       = Column(Integer, default=0)
    registros_fallidos        = Column(Integer, default=0)
    tiempo_ejecucion_segundos = Column(Float, default=0.0)
