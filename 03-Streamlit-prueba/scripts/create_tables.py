from database import engine
from sqlalchemy import text

create_table_query = """
CREATE TABLE IF NOT EXISTS clima (
    id SERIAL PRIMARY KEY,
    ciudad VARCHAR(50),
    pais VARCHAR(50),
    temperatura FLOAT,
    sensacion_termica FLOAT,
    humedad INT,
    velocidad_viento FLOAT,
    descripcion VARCHAR(100),
    fecha_extraccion TIMESTAMP
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))
    conn.commit()

print("✅ Tabla creada")
