import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de conexión
DB_URL = os.getenv('DATABASE_URL', 'postgresql://etl_user:etl_password@localhost:5432/weatherstack_dw')
engine = create_engine(DB_URL)

def cargar_a_postgres():
    if not os.path.exists('data/clima.csv'):
        print("❌ Error: No se encontró data/clima.csv")
        return

    df = pd.read_csv('data/clima.csv')
    
    with engine.begin() as conn:
        print("Subiendo ciudades...")
        for _, row in df[['ciudad', 'pais']].drop_duplicates().iterrows():
            # Versión compatible: Primero intentamos insertar, si falla, seguimos
            try:
                conn.execute(text("""
                    INSERT INTO ciudades (nombre, pais) 
                    VALUES (:nombre, :pais) 
                    ON CONFLICT DO NOTHING
                """), {"nombre": row['ciudad'], "pais": row['pais']})
            except:
                pass

        print("Subiendo datos de clima...")
        # Insertar datos de clima
        df.to_sql('clima', engine, if_exists='append', index=False)

        print("Vinculando registros...")
        # Vincular con ciudad_id
        conn.execute(text("""
            UPDATE clima 
            SET ciudad_id = ciudades.id 
            FROM ciudades 
            WHERE clima.ciudad = ciudades.nombre 
            AND clima.ciudad_id IS NULL
        """))
        print(f"✅ ¡Éxito! {len(df)} registros procesados.")

if __name__ == "__main__":
    cargar_a_postgres()