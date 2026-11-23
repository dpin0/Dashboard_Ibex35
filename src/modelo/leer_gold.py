from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from src.modelo.ejercicios_pract4 import config_pract4 as cfg


def leer_tabla(spark: SparkSession, tabla: str) -> DataFrame:
    ruta = f"{cfg.RUTA_GOLD}/{tabla}"
    lector = spark.read.format(cfg.FORMATO_GOLD)
    if cfg.FORMATO_GOLD == "csv":
        lector = lector.option("header", True).option("inferSchema", True)
    return lector.load(ruta)


def cargar_apertura_cierre(spark: SparkSession, empresa: str = cfg.VALOR_EMPRESA) -> DataFrame:
    """Open y Close (como double) de la empresa indicada, sin nulos."""
    df = leer_tabla(spark, cfg.TABLA_HECHOS).filter(F.col(cfg.COL_TICKER) == empresa)
    for c in cfg.FEATURES:
        df = df.withColumn(c, F.col(c).cast("double"))
    return df.select(*cfg.FEATURES).dropna()

# Lectura de la capa gold (data/export/gold) y construcción del dataset de BBVA.