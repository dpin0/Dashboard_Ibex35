import os
from delta.tables import DeltaTable

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"
RUTA_BRONZE_SENTIMIENTO = "data/lake/bronze/sentimiento"   


def ejercicio3(spark, rutas=None):
    if rutas is None:
        rutas = {
            "ibex": RUTA_BRONZE_IBEX,
            "sentimiento": RUTA_BRONZE_SENTIMIENTO,
        }

    resultados = {}
    for nombre, ruta in rutas.items():
        DeltaTable.convertToDelta(spark, f"parquet.`{ruta}`")

        historial = DeltaTable.forPath(spark, ruta).history()
        contenido_log = sorted(os.listdir(os.path.join(ruta, "_delta_log")))

        resultados[nombre] = (historial, contenido_log)

    return resultados