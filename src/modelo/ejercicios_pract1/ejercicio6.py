from delta.tables import DeltaTable

from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, historial)


def ejercicio6(spark, version, filas_ej4, ruta=RUTA_BRONZE_IBEX):
    tabla = DeltaTable.forPath(spark, ruta)
    filas_antes = spark.read.format("delta").load(ruta).count()

    tabla.restoreToVersion(version)

    df = spark.read.format("delta").load(ruta)

    return {
        "version": version,
        "filas_antes": filas_antes,
        "filas_despues": df.count(),
        "filas_ej4": filas_ej4,
        "bbva": df.filter("Ticker = 'BBVA.MC'").count(),
        "columnas": df.columns,
        "historial": historial(spark,ruta),
    }