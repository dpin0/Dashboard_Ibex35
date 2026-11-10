from pyspark.sql import functions as F

RUTA_SILVER_IBEX = "data/lake/silver/ibex"
RUTA_SILVER_EMPRESAS = "data/lake/silver/empresas"
RUTA_SILVER_SENTIMIENTO = "data/lake/silver/sentimiento"
RUTA_GOLD = "data/lake/gold"


def _leer(spark, ruta):
    return spark.read.format("delta").load(ruta)   # cambia a .parquet(ruta) si no usas delta en silver

#Ej10
def ejercicio10(spark):
    ibex = _leer(spark, RUTA_SILVER_IBEX).withColumn("Fecha", F.to_date("Fecha"))
    empresas = _leer(spark, RUTA_SILVER_EMPRESAS)

    # Una fila por (Fecha, Sector) para no multiplicar filas en el join
    sent = (
        _leer(spark, RUTA_SILVER_SENTIMIENTO)
        .withColumn("Fecha", F.to_date("Fecha"))
        .groupBy("Fecha", "Sector")
        .agg(F.round(F.avg("Sentimiento"), 2).alias("Sentimiento"))
    )

    gold = (
        ibex
        .join(empresas, on="Ticker", how="left")
        .join(sent, on=["Fecha", "Sector"], how="left")
        .withColumn("Anio", F.year("Fecha"))
        .select(
            "Fecha", "Ticker", "Nombre", "Sector", "Industria",
            "Capitalizacion", "Recomendacion",
            "Open", "High", "Low", "Close", "Volume",
            "Dividends", "Stock_Splits", "Sentimiento", "Anio",
        )
    )

    (gold.write.format("delta")
         .mode("overwrite")
         .option("overwriteSchema", "true")
         .partitionBy("Anio")
         .save(RUTA_GOLD))

    leido = _leer(spark, RUTA_GOLD)
    return {
        "filas_ibex": ibex.count(),
        "filas_gold": leido.count(),
        "columnas": leido.columns,
        "sin_empresa": leido.filter(F.col("Nombre").isNull()).count(),
        "sin_sentimiento": leido.filter(F.col("Sentimiento").isNull()).count(),
        "ruta": RUTA_GOLD,
        "muestra": leido.orderBy(F.desc("Fecha")).limit(5),
    }