RUTA_BRONZE_SENTIMIENTO = "data/lake/bronze/sentimiento"

def ejercicio2b(df, ruta=RUTA_BRONZE_SENTIMIENTO):

    n_filas = df.count()
    df.write.mode("overwrite").parquet(ruta)
    return n_filas