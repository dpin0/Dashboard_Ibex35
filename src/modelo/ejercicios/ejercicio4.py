from delta.tables import DeltaTable
from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, contar_filas, version_actual, historial)


def _merge_nuevos(spark, nuevos, ruta):
    destino = DeltaTable.forPath(spark, ruta)
    (destino.alias("d")
        .merge(nuevos.alias("n"),
               "d.Ticker = n.Ticker AND d.Date = n.Date")
        .whenNotMatchedInsertAll()
        .execute())
    return contar_filas(spark, ruta)


# Ej4
def ejercicio4(spark, nuevos, ruta=RUTA_BRONZE_IBEX):
    # Evita insertar dos veces la misma clave si la descarga trae repetidos
    nuevos = nuevos.dropDuplicates(["Ticker", "Date"])

    # Version actual y filas antes de cargar
    version_antes = version_actual(spark, ruta)
    historial_actual = DeltaTable.forPath(spark, ruta).history(1).toPandas()
    filas_inicial = contar_filas(spark, ruta)

    # 1ª ejecucion: deben insertarse los dias nuevos
    filas_tras_1 = _merge_nuevos(spark, nuevos, ruta)
    # Version justo tras el MERGE (la que se usara en el Ej6)
    version_tras_1 = version_actual(spark, ruta)

    # 2ª ejecucion: no debe cambiar nada (idempotente)
    filas_tras_2 = _merge_nuevos(spark, nuevos, ruta)

    return {
        "version_actual": version_antes,
        "historial_actual": historial_actual,
        "version_tras_1": version_tras_1,
        "filas_inicial": filas_inicial,
        "filas_tras_1": filas_tras_1,
        "filas_tras_2": filas_tras_2,
        "historial": historial,
    }