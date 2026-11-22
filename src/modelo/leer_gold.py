"""Lectura de la capa gold (data/export/gold) y construcción del dataset de BBVA."""
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
    """Apertura y cierre (como double) de la empresa indicada, sin nulos."""
    hechos = leer_tabla(spark, cfg.TABLA_HECHOS)
    dim_emp = leer_tabla(spark, cfg.TABLA_EMPRESA).filter(F.col(cfg.COL_NOMBRE_EMPRESA) == empresa)
    df = hechos.join(dim_emp.select(cfg.COL_CLAVE_EMPRESA), on=cfg.COL_CLAVE_EMPRESA, how="inner")
    for c in cfg.FEATURES:
        df = df.withColumn(c, F.col(c).cast("double"))
    return df.select(*cfg.FEATURES).dropna()