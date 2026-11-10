from delta.tables import DeltaTable

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"


def ejercicio5d(spark, version_antes_5a, ruta=RUTA_BRONZE_IBEX):
    historial = DeltaTable.forPath(spark, ruta).history()

    df_antigua = spark.read.format("delta") \
        .option("versionAsOf", version_antes_5a).load(ruta)
    df_actual = spark.read.format("delta").load(ruta)

    return {
        "version_antes_5a": version_antes_5a,
        "historial": historial,
        "columnas_antigua": df_antigua.columns,
        "columnas_actual": df_actual.columns,
        "filas_antigua": df_antigua.count(),
        "filas_actual": df_actual.count(),
        "bbva_antigua": df_antigua.filter("Ticker = 'BBVA.MC'").count(),
        "bbva_actual": df_actual.filter("Ticker = 'BBVA.MC'").count(),
    }
