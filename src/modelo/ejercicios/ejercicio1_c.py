RUTA_BRONZE = "data/lake/bronze/ibex"


def leer_1c(spark, ruta=RUTA_BRONZE):

    df = spark.read.parquet(ruta)
    df_det = spark.read.parquet(ruta).select("Ticker", "Date", "Close")
    return df, df_det