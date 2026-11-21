from delta.tables import DeltaTable
from pyspark.sql.functions import col

from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX)


def ejercicio5b(spark, ruta=RUTA_BRONZE_IBEX):
    columnas_antes = spark.read.format("delta").load(ruta).columns
    filas_antes = spark.read.format("delta").load(ruta).count()

    df = spark.read.format("delta").load(ruta) \
        .withColumn("Close_mas5", col("Close") + 5)

    rechazado = False
    try:
        df.write.format("delta").mode("append") \
            .option("mergeSchema", "true").save(ruta)
    except Exception as e:
        rechazado = True

    tabla_nueva = spark.read.format("delta").load(ruta)
    columnas_despues = tabla_nueva.columns
    filas_despues = tabla_nueva.count()
    nulos_close_mas5 = tabla_nueva.filter(col("Close_mas5").isNull()).count()

    return {
        "rechazado": rechazado,
        "columnas_antes": columnas_antes,
        "columnas_despues": columnas_despues,
        "filas_antes": filas_antes,
        "filas_despues": filas_despues,
        "nulos_close_mas5": nulos_close_mas5,
    }

