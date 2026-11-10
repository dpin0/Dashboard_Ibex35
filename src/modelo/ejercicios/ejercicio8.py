from pyspark.sql import functions as F
from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, RUTA_BRONZE_SENTIMIENTO, RUTA_SILVER_SENTIMIENTO,
    traducir_sectores, escribir_delta, leer_delta, contar_filas)


def ejercicio8(spark):
    bronze = leer_delta(spark, RUTA_BRONZE_SENTIMIENTO)
    limpio = (traducir_sectores(bronze.dropna())
              .dropDuplicates(["Fecha", "Sector"]))
    escribir_delta(limpio, RUTA_SILVER_SENTIMIENTO)

    silver = leer_delta(spark, RUTA_SILVER_SENTIMIENTO)
    ibex = leer_delta(spark, RUTA_BRONZE_IBEX)
    return {
        "filas_ibex": contar_filas(spark, RUTA_BRONZE_IBEX),
        "filas_bronze": bronze.count(),
        "filas_silver": silver.count(),
        "rango_sent": silver.agg(F.min("Fecha"), F.max("Fecha")).first(),
        "rango_ibex": ibex.agg(F.min("Date"), F.max("Date")).first(),
        "por_sector": [(r["Sector"], r["count"])
                       for r in silver.groupBy("Sector").count().orderBy("Sector").collect()],
        "silver": silver,
    }