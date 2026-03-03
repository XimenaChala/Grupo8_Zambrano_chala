from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Ciudad(Base):
    __tablename__ = 'ciudades'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    pais = Column(String)

class RegistroClima(Base):
    __tablename__ = 'clima'
    id = Column(Integer, primary_key=True)
    ciudad_id = Column(Integer, ForeignKey('ciudades.id')) 
    ciudad = Column(String) 
    pais = Column(String)   
    temperatura = Column(Float)
    sensacion_termica = Column(Float) 
    humedad = Column(Integer)
    velocidad_viento = Column(Float)  
    descripcion = Column(String)
    fecha_extraccion = Column(DateTime)

class MetricasETL(Base):
    __tablename__ = 'metricas_etl'
    id = Column(Integer, primary_key=True)
    fecha_ejecucion = Column(DateTime, default=datetime.utcnow)