from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from src.modelo.ejercicios_pract3.config_pract3 import COL_TICKER, VALOR_EMPRESA, FORMATO_GOLD, RUTA_GOLD, FEATURES, TABLA_HECHOS


def leer_tabla(spark: SparkSession, tabla: str) -> DataFrame:
    ruta = f"{RUTA_GOLD}/{tabla}"
    lector = spark.read.format(FORMATO_GOLD)
    if FORMATO_GOLD == "csv":
        lector = lector.option("header", True).option("inferSchema", True)
    return lector.load(ruta)


def cargar_apertura_cierre(spark: SparkSession, empresa: str = VALOR_EMPRESA) -> DataFrame:
    """Open y Close (como double) de la empresa indicada, sin nulos."""
    df = leer_tabla(spark, TABLA_HECHOS).filter(F.col(COL_TICKER) == empresa)
    for c in FEATURES:
        df = df.withColumn(c, F.col(c).cast("double"))
    return df.select(*FEATURES).dropna()

# Lectura de la capa gold (data/export/gold) y construcción del dataset de BBVA.