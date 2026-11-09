from delta.tables import DeltaTable

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"


def ejercicio6(spark, version, filas_ej4, ruta=RUTA_BRONZE_IBEX):
    tabla = DeltaTable.forPath(spark, ruta)
    filas_antes = spark.read.format("delta").load(ruta).count()

    tabla.restoreToVersion(version)

    df = spark.read.format("delta").load(ruta)
    historial = DeltaTable.forPath(spark, ruta).history()

    return {
        "version": version,
        "filas_antes": filas_antes,
        "filas_despues": df.count(),
        "filas_ej4": filas_ej4,
        "bbva": df.filter("Ticker = 'BBVA'").count(),
        "columnas": df.columns,
        "historial": historial,
    }