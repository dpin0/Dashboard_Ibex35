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

os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
MLFLOW_URI = str(Path("mlruns").resolve())

COLS_BASE_CORR = ["Open", "High", "Low", "Close", "Volume", "Sentimiento"]
COLS_CORRELACION = ["Open", "High", "Low", "Close", "Volume",
                    "Return", "RangeLow", "RangeOpen", "Sentimiento"]
COLS_BASE_RETURN = ["Open", "Close", "Sentimiento"]