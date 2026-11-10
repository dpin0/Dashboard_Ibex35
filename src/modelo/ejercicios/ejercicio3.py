import os
from delta.tables import DeltaTable
from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, RUTA_BRONZE_SENTIMIENTO, historial)

def ejercicio3(spark, rutas=None):
    if rutas is None:
        rutas = {
            "ibex": RUTA_BRONZE_IBEX,
            "sentimiento": RUTA_BRONZE_SENTIMIENTO,
        }

    resultados = {}
    for nombre, ruta in rutas.items():
        DeltaTable.convertToDelta(spark, f"parquet.`{ruta}`")

        contenido_log = sorted(os.listdir(os.path.join(ruta, "_delta_log")))

        resultados[nombre] = (historial(spark,ruta), contenido_log)

    return resultados