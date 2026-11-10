from pyspark.sql import functions as F
from src.modelo.funciones_delta import (
    RUTA_GOLD_HECHO, RUTA_GOLD_DIM_EMPRESA, RUTA_EXPORT,
    leer_delta, construir_dim_fecha, exportar_parquet,
)

#Ej13
def ejercicio13(spark):
    hecho = leer_delta(spark, RUTA_GOLD_HECHO)
    dim_empresa = leer_delta(spark, RUTA_GOLD_DIM_EMPRESA)

    # Hecho: solo claves + medidas, redondeadas y ordenadas (comprime mejor)
    for c in ["Open", "High", "Low", "Close", "Var_diaria", "Media_movil_7"]:
        hecho = hecho.withColumn(c, F.round(c, 2))
    hecho = (hecho.withColumn("Var_pct", F.round("Var_pct", 3)).orderBy("Ticker", "FechaKey"))

    # Calendario continuo (sin saltos) entre la primera y la última sesión
    fechas = (hecho.select(F.to_date(F.col("FechaKey").cast("string"), "yyyyMMdd").alias("Fecha"))
                   .agg(F.min("Fecha").alias("a"), F.max("Fecha").alias("b"))
                   .select(F.explode(F.sequence("a", "b", F.expr("interval 1 day"))).alias("Fecha")))
    dim_fecha = construir_dim_fecha(fechas)

    rutas = {
        "fact_cotizaciones": hecho,
        "dim_empresa": dim_empresa,
        "dim_fecha": dim_fecha,
    }
    filas = {}
    for nombre, df in rutas.items():
        ruta = f"{RUTA_EXPORT}/{nombre}"
        exportar_parquet(df, ruta)
        filas[nombre] = spark.read.parquet(ruta).count()

    return {"filas": filas, "ruta": RUTA_EXPORT,
            "esquema_hecho": spark.read.parquet(f"{RUTA_EXPORT}/fact_cotizaciones").dtypes}