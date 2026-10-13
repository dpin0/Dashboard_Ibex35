RUTA_BRONZE_SENTIMIENTO = "data/lake/bronze/sentimiento"

def ejercicio2c(spark, df, ruta=RUTA_BRONZE_SENTIMIENTO):
    
    antes = spark.read.parquet(ruta).count()
    df.write.mode("append").parquet(ruta)
    despues = spark.read.parquet(ruta).count()
    return antes, despues