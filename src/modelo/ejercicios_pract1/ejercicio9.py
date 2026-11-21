from src.modelo.ejercicios.ejercicio1_b import TICKERS
from src.modelo.funciones_delta import (
    RUTA_BRONZE_IBEX, RUTA_BRONZE_EMPRESAS, RUTA_SILVER_IBEX,
    RUTA_SILVER_EMPRESAS, leer_delta, escribir_delta, contar_filas, limpiar_precios, descargar_info_empresas, empresas_silver)

# Ej9
def ejercicio9(spark):
    # La fecha de Yahoo es un timestamp: fijar la zona
    spark.conf.set("spark.sql.session.timeZone", "Europe/Madrid")

    # Precios: bronze -> silver
    precios = limpiar_precios(leer_delta(spark, RUTA_BRONZE_IBEX))
    escribir_delta(precios, RUTA_SILVER_IBEX)

    # Empresas: crudo en bronze, corregido en silver
    crudo = descargar_info_empresas(spark, TICKERS)
    escribir_delta(crudo, RUTA_BRONZE_EMPRESAS)
    escribir_delta(empresas_silver(leer_delta(spark, RUTA_BRONZE_EMPRESAS)),
                   RUTA_SILVER_EMPRESAS)

    return {
        "filas_ibex": contar_filas(spark, RUTA_SILVER_IBEX),
        "filas_empresas": contar_filas(spark, RUTA_SILVER_EMPRESAS),
        "ibex": leer_delta(spark, RUTA_SILVER_IBEX),
        "empresas": leer_delta(spark, RUTA_SILVER_EMPRESAS),
    }
