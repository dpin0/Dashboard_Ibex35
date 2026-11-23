from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

RUTA_FEATURES = "data/lake/features"

def guardar_features(df: DataFrame, version: int, ruta: str = RUTA_FEATURES) -> None:
    """Guarda las features con una columna `version`.
    Usa replaceWhere: si se vuelve a guardar la misma versión la sustituye (no se
    duplica) y las demás versiones no se tocan."""
    (df.withColumn("version", F.lit(version))
       .write.format("delta")
       .mode("overwrite")
       .option("replaceWhere", f"version = {version}")
       .save(ruta))


def recuperar_features(spark: SparkSession, version: int, ruta: str = RUTA_FEATURES) -> DataFrame:
    """Lee de la tabla únicamente la versión pedida (sin la columna version)."""
    return (spark.read.format("delta").load(ruta)
            .filter(F.col("version") == version)
            .drop("version"))