from delta.tables import DeltaTable
from pyspark.sql.functions import col
from pyspark.errors import AnalysisException

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"


def ejercicio5a(spark, ruta=RUTA_BRONZE_IBEX):
    # Versión y filas ANTES de intentar escribir (la usarás en el Ej5d)
    version_antes = DeltaTable.forPath(spark, ruta).history(1) \
        .select("version").collect()[0][0]
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

    version_despues = DeltaTable.forPath(spark, ruta).history(1) \
        .select("version").collect()[0][0]
    filas_despues = spark.read.format("delta").load(ruta).count()

    return {
        "version_antes": version_antes,
        "version_despues": version_despues,
        "filas_antes": filas_antes,
        "filas_despues": filas_despues,
        "rechazado": rechazado,
        "mensaje": mensaje,
    }
