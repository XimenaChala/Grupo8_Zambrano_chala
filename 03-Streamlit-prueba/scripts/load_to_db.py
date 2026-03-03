import pandas as pd
from database import engine

df = pd.read_csv("data/clima.csv")

df.to_sql("clima", engine, if_exists="append", index=False)

print("✅ Datos cargados en PostgreSQL")
