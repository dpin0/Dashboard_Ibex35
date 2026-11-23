import os

RUTA_GOLD = "data/export/gold"
FORMATO_GOLD = "parquet" # "csv" | "parquet" | "delta"
TABLA_HECHOS = "fact_cotizaciones"

COL_TICKER = "Ticker"        
VALOR_EMPRESA = "BBVA.MC"               
COL_APERTURA = "Open"           
COL_CIERRE = "Close"   

FEATURES = [COL_APERTURA, COL_CIERRE]

SEED_MODELO = 1
SEED_HYPEROPT = 42

from pathlib import Path
MLFLOW_URI = "sqlite:///" + Path("mlflow.db").resolve().as_posix()
EXPERIMENTO_EJ1 = "kmeans_BBVA_ej1"
EXPERIMENTO_EJ2 = "kmeans_BBVA"