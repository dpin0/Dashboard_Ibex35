from delta.tables import DeltaTable
from pyspark.sql.functions import col
from pyspark.errors import AnalysisException

from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, version_actual)



def ejercicio5a(spark, ruta=RUTA_BRONZE_IBEX):
    filas_antes = spark.read.format("delta").load(ruta).count()

    # Columna nueva: Close + 5
    df = spark.read.format("delta").load(ruta) \
        .withColumn("Close_mas5", col("Close") + 5)

    rechazado = False
    mensaje = ""
    try:
        df.write.format("delta").mode("append").save(ruta)
    except AnalysisException as e:
        rechazado = True
        mensaje = str(e).split("\n")[0]

    filas_despues = spark.read.format("delta").load(ruta).count()

    return {
        "version_antes": version_actual,
        "version_despues": version_actual,
        "filas_antes": filas_antes,
        "filas_despues": filas_despues,
        "rechazado": rechazado,
        "mensaje": mensaje,
    }
