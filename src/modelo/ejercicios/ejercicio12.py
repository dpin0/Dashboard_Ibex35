from pyspark.sql import functions as F
from src.modelo.funciones_delta import (
    RUTA_GOLD_HECHO, leer_delta, escribir_delta, rellenar_sentimiento,
)

# Ej12 
def ejercicio12(spark):
    h = leer_delta(spark, RUTA_GOLD_HECHO)

    h = h.withColumn("Sentimiento_imputado", F.col("Sentimiento").isNull())
    h = rellenar_sentimiento(h)

    h = (h
         # Amplitud del día en %: mide la volatilidad intradía
         .withColumn("Rango_pct",
                     F.round(F.try_divide(F.col("High") - F.col("Low"),
                                          F.col("Low")) * 100, 2))
         # Close sobre su media de 7 sesiones: señal simple para colorear
         .withColumn("Tendencia",
                     F.when(F.col("Close") > F.col("Media_movil_7"), "Alcista")
                      .otherwise("Bajista")))

    escribir_delta(h, RUTA_GOLD_HECHO)

    leido = leer_delta(spark, RUTA_GOLD_HECHO)
    return {
        "columnas": leido.columns,
        "imputadas": leido.filter("Sentimiento_imputado").count(),
        "muestra": (leido.select("Ticker", "FechaKey", "Close", "Var_diaria",
                                 "Var_pct", "Media_movil_7", "Rango_pct",
                                 "Tendencia", "Sentimiento", "Sentimiento_imputado")
                         .orderBy(F.desc("FechaKey")).limit(5)),
    }