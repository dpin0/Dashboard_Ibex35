from pyspark.sql import functions as F

from src.modelo.funciones_delta import (
    RUTA_SILVER_IBEX, RUTA_SILVER_EMPRESAS, RUTA_SILVER_SENTIMIENTO,
    RUTA_GOLD_HECHO, RUTA_GOLD_DIM_EMPRESA, RUTA_GOLD_DIM_FECHA, RUTA_GOLD,
    leer_delta, escribir_delta, anti_join,
    construir_dim_fecha, construir_hecho, anadir_calculos,
)

#Ej10
def ejercicio10(spark):
    precios = leer_delta(spark, RUTA_SILVER_IBEX)
    empresas = leer_delta(spark, RUTA_SILVER_EMPRESAS)

    sentimiento = (
        leer_delta(spark, RUTA_SILVER_SENTIMIENTO)
        .groupBy("Sector", "Fecha")
        .agg(F.round(F.avg("Sentimiento"), 2).alias("Sentimiento"))
    )

    dim_empresa = empresas.select(
        "Ticker", "Nombre", "Sector", "Industria", "Capitalizacion", "Recomendacion")
    dim_fecha = construir_dim_fecha(precios)

    hecho = anadir_calculos(construir_hecho(precios, empresas, sentimiento))

    escribir_delta(dim_empresa, RUTA_GOLD_DIM_EMPRESA)
    escribir_delta(dim_fecha, RUTA_GOLD_DIM_FECHA)
    escribir_delta(hecho, RUTA_GOLD_HECHO)

    # Verificación
    h = leer_delta(spark, RUTA_GOLD_HECHO)
    d_emp = leer_delta(spark, RUTA_GOLD_DIM_EMPRESA)
    d_fec = leer_delta(spark, RUTA_GOLD_DIM_FECHA)

    return {
        "filas_silver": precios.count(),
        "filas_hecho": h.count(),
        "filas_dim_empresa": d_emp.count(),
        "filas_dim_fecha": d_fec.count(),
        "claves_duplicadas": h.count() - h.select("Ticker", "FechaKey").distinct().count(),
        "huerfanos_empresa": anti_join(h, d_emp, ["Ticker"]).count(),
        "huerfanos_fecha": anti_join(h, d_fec, ["FechaKey"]).count(),
        "sin_sentimiento": h.filter(F.col("Sentimiento").isNull()).count(),
        "ruta": RUTA_GOLD,
        "muestra": h.orderBy(F.desc("FechaKey")).limit(5),
    }