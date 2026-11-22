import os

RUTA_GOLD = "data/export/gold"
FORMATO_GOLD = "csv"                 # "csv" | "parquet" | "delta"
TABLA_HECHOS = "fact_cotizaciones"
TABLA_EMPRESA = "dim_empresa"
COL_CLAVE_EMPRESA = "id_empresa"     # <-- clave común fact/dim_empresa
COL_NOMBRE_EMPRESA = "ticker"        # <-- columna de dim_empresa para filtrar
VALOR_EMPRESA = "BBVA"               # <-- p. ej. "BBVA" o "BBVA.MC"
COL_APERTURA = "apertura"            # <-- columna Valor de Apertura (fact)
COL_CIERRE = "cierre"                # <-- columna Valor de Cierre (fact)
FEATURES = [COL_APERTURA, COL_CIERRE]

SEED_MODELO = 1
SEED_HYPEROPT = 42

MLFLOW_URI = f"file:///{os.path.abspath('mlruns')}"
EXPERIMENTO_EJ1 = "kmeans_BBVA_ej1"
EXPERIMENTO_EJ2 = "kmeans_BBVA"