from delta.tables import DeltaTable

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"


def ejercicio5c(spark, ruta=RUTA_BRONZE_IBEX):
    tabla = DeltaTable.forPath(spark, ruta)

    antes = tabla.toDF().filter("Ticker = 'BBVA.MC'")
    filas_bbva_antes = antes.count()
    muestra_antes = antes.limit(5).toPandas()

    tabla.delete("Ticker = 'BBVA.MC'")

    despues = DeltaTable.forPath(spark, ruta).toDF().filter("Ticker = 'BBVA.MC'")
    filas_bbva_despues = despues.count()
    muestra_despues = despues.limit(5).toPandas()

    return {
        "filas_bbva_antes": filas_bbva_antes,
        "filas_bbva_despues": filas_bbva_despues,
        "muestra_antes": muestra_antes,
        "muestra_despues": muestra_despues,
    }
