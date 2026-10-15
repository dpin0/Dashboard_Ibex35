from delta.tables import DeltaTable

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"


def _merge_nuevos(spark, nuevos, ruta):
    destino = DeltaTable.forPath(spark, ruta)
    (destino.alias("d")
        .merge(nuevos.alias("n"),
               "d.Ticker = n.Ticker AND d.Fecha = n.Fecha")
        .whenNotMatchedInsertAll()
        .execute())
    return spark.read.format("delta").load(ruta).count()


def ejercicio4(spark, nuevos, ruta=RUTA_BRONZE_IBEX):
    # Evita insertar dos veces la misma clave si la descarga trae repetidos
    nuevos = nuevos.dropDuplicates(["Ticker", "Fecha"])

    tabla = DeltaTable.forPath(spark, ruta)

    # Versión actual (entero) y filas antes de cargar
    version_actual = tabla.history(1).select("version").collect()[0][0]
    filas_inicial = spark.read.format("delta").load(ruta).count()

    # 1ª ejecución: deben insertarse los días nuevos
    filas_tras_1 = _merge_nuevos(spark, nuevos, ruta)

    # 2ª ejecución: no debe cambiar nada (idempotente)
    filas_tras_2 = _merge_nuevos(spark, nuevos, ruta)

    historial = DeltaTable.forPath(spark, ruta).history()

    return {
        "version_actual": version_actual,
        "filas_inicial": filas_inicial,
        "filas_tras_1": filas_tras_1,
        "filas_tras_2": filas_tras_2,
        "historial": historial,
    }