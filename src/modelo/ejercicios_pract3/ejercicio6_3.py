#ejercicio 6 - práctica 3

from pyspark.sql import functions as F
from src.modelo.leer_gold import leer_tabla
from src.modelo.estadisticas import crear_variables_derivadas, matriz_correlacion
from src.modelo.ejercicios_pract3.config_pract3 import COLS_BASE_CORR, VALOR_EMPRESA, TABLA_HECHOS, COL_TICKER

def ejercicio6_3(spark, empresa:str = VALOR_EMPRESA) -> dict:
    df = (leer_tabla(spark, TABLA_HECHOS)
          .filter(F.col(COL_TICKER) == empresa)
          .select(* [F.col(c).cast("double").alias(c) for c in COLS_BASE_CORR])
          .dropna()
          .filter((F.col("Open")>0) & ((F.col("Low")>0)))
          )

    df = crear_variables_derivadas(df).cache()
    
    return {"empresa": empresa, "n_filas": df.count(), "matriz": matriz_correlacion(df)}

