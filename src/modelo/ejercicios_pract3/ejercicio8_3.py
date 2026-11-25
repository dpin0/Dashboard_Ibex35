#ejercicio 8 - práctica 3

from pyspark.sql import functions as F
from src.modelo.leer_gold import leer_tabla
from src.modelo.estadisticas import (crear_return, crear_anio_mes, agrupar_sector_mes, correlacion_pearson)
from src.modelo.ejercicios_pract3.config_pract3 import TABLA_HECHOS, COL_TICKER, COL_FECHAKEY, COLS_BASE_RETURN, COL_SECTOR, TABLA_EMPRESA, COL_FECHAKEY


def ejercicio8_3(spark) -> dict:
    # Filas empresa-día de todas las empresas
    hechos = (leer_tabla(spark, TABLA_HECHOS)
              .select(COL_TICKER, COL_FECHAKEY,
                      *[F.col(c).cast("double").alias(c) for c in COLS_BASE_RETURN])
              .dropna()
              .filter(F.col("Open") > 0))
    # Sector de cada empresa (dim_empresa) y Return/Anio/Mes de cada fila
    sectores = leer_tabla(spark, TABLA_EMPRESA).select(COL_TICKER, COL_SECTOR)
    filas = crear_anio_mes(crear_return(hechos.join(sectores, on=COL_TICKER, how="inner")), COL_FECHAKEY)

    # Tabla con una fila por (sector, mes) y correlación entre las dos medias
    tabla = agrupar_sector_mes(filas, COL_SECTOR).cache()
    return {"n_filas": filas.count(), "n_grupos": tabla.count(),
            "tabla": tabla.toPandas(),
            "correlacion": correlacion_pearson(tabla, "SentMedioMes", "RetMedioMes")}