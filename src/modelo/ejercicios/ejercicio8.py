from pyspark.sql import functions as F
from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, RUTA_BRONZE_SENTIMIENTO, RUTA_SILVER_SENTIMIENTO,
    limpiar_sentimiento, escribir_delta, leer_delta, contar_filas)

# Ej8
def ejercicio8(spark):
    bronze = leer_delta(spark, RUTA_BRONZE_SENTIMIENTO)
    escribir_delta(limpiar_sentimiento(bronze), RUTA_SILVER_SENTIMIENTO)

    silver = leer_delta(spark, RUTA_SILVER_SENTIMIENTO)
    ibex = leer_delta(spark, RUTA_BRONZE_IBEX)
    filas_bronze = bronze.count()
    filas_silver = silver.count()
    return {
        "filas_ibex": contar_filas(spark, RUTA_BRONZE_IBEX),
        "filas_bronze": filas_bronze,
        "filas_silver": filas_silver,
        "filas_descartadas": filas_bronze - filas_silver,
        "tipos_silver": silver.dtypes,
        "rango_sent": silver.agg(F.min("Fecha"), F.max("Fecha")).first(),
        "rango_ibex": ibex.agg(F.min("Date"), F.max("Date")).first(),
        "por_sector": [(r["Sector"], r["count"])
                       for r in silver.groupBy("Sector").count().orderBy("Sector").collect()],
        "silver": silver,
    }