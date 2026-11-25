#ejercicio 7 - práctica 3

from pyspark.sql import functions as F
from src.modelo.leer_gold import leer_tabla
from src.modelo.estadisticas import crear_return, correlacion_pearson
from src.modelo.ejercicios_pract3.config_pract3 import TABLA_HECHOS, COL_TICKER, COLS_BASE_RETURN

def ejercicio7_3(spark) -> dict:
    df = (leer_tabla(spark, TABLA_HECHOS)
          .select(COL_TICKER, *[F.col(c).cast("double").alias(c) for c in COLS_BASE_RETURN])
          .dropna()
          .filter(F.col("Open") > 0))

    df = crear_return(df).cache()

    return{"n_filas": df.count(),
           "n_empresas": df.select(COL_TICKER).distinct().count(),
           "correlacion": correlacion_pearson(df, "Sentimiento", "Return")}
    