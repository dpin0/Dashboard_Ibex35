from src.modelo.funciones_delta import (
    RUTA_CSV_SENTIMIENTO)

def ejercicio2a(spark, ruta=RUTA_CSV_SENTIMIENTO):

    return spark.read.option("header", True).option("sep", ";").option("inferSchema", True).csv(ruta)