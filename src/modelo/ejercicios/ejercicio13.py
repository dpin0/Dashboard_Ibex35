from src.modelo.funciones_delta import (
    RUTA_GOLD, RUTA_EXPORT, leer_delta, exportar_parquet)

TABLAS_GOLD = ["fact_cotizaciones", "dim_empresa", "dim_fecha"]


# Ej13
def ejercicio13(spark):
    for t in TABLAS_GOLD:
        exportar_parquet(leer_delta(spark, f"{RUTA_GOLD}/{t}"), f"{RUTA_EXPORT}/{t}")
    return {t: spark.read.parquet(f"{RUTA_EXPORT}/{t}").count() for t in TABLAS_GOLD}


def mostrar_ejercicio_13(r):
    print("=== Ejercicio 13: export a Parquet ===")
    for tabla, n in r.items():
        print(f"data/export/gold/{tabla}: {n} filas")
