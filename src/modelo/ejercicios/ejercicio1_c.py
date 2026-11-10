from src.modelo.funciones_delta import(
    RUTA_BRONZE_IBEX)


def leer_1c(spark, ruta=RUTA_BRONZE_IBEX):

    df = spark.read.parquet(ruta)
    df_det = spark.read.parquet(ruta).select("Ticker", "Date", "Close")
    return df, df_det