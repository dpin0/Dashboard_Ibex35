RUTA_CSV = "data/sentimiento_ibex.csv"

def ejercicio2a(spark, ruta=RUTA_CSV):

    return spark.read.option("header", True).csv(ruta)