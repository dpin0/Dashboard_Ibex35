from delta.tables import DeltaTable
from pyspark.sql.functions import col
from pyspark.sql.utils import AnalysisException

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


def mostrar_ejercicio_5a(r):
    print("=== Ejercicio 5a: append con columna extra (Close_mas5) ===")
    print(f"¿Delta lo ha rechazado? {r['rechazado']}")
    print(f"Mensaje: {r['mensaje']}")
    print(f"Versión antes: {r['version_antes']} | después: {r['version_despues']}")
    print(f"Filas antes: {r['filas_antes']} | después: {r['filas_despues']}")
    print("\nComentario: Delta aplica schema enforcement: rechaza escribir "
          "una columna que no existe en el esquema de la tabla. Al fallar, "
          "no se crea ninguna versión y la tabla queda intacta.")