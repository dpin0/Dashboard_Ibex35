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
    historial_actual = tabla.history(1).toPandas()   
    filas_inicial = spark.read.format("delta").load(ruta).count()

    # 1ª ejecución: deben insertarse los días nuevos
    filas_tras_1 = _merge_nuevos(spark, nuevos, ruta)

    version_tras_1 = DeltaTable.forPath(spark, ruta).history(1) \
        .select("version").collect()[0][0]
    
    # versión justo tras el MERGE (la que se usará en el Ej6)
    version_tras_1 = DeltaTable.forPath(spark, ruta).history(1) \
        .select("version").collect()[0][0]

    # 2ª ejecución: no debe cambiar nada (idempotente)
    filas_tras_2 = _merge_nuevos(spark, nuevos, ruta)

    historial = DeltaTable.forPath(spark, ruta).history()

    return {
        "historial_actual": historial_actual,                           # NUEVO
        "version_tras_1": version_tras_1,    
        "filas_inicial": filas_inicial,
        "filas_tras_1": filas_tras_1,
        "filas_tras_2": filas_tras_2,
        "historial": historial,
    }