"""Variables derivadas y correlaciones (lógica estadística reutilizable)."""
import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
from pyspark.sql import functions as F
from src.modelo.ejercicios_pract3.config_pract3 import COLS_CORRELACION


def crear_return(df):
    """Return=(Close-Open)/Open."""
    return df.withColumn("Return", (F.col("Close") - F.col("Open")) / F.col("Open"))


def crear_variables_derivadas(df):
    """Return=(Close-Open)/Open, RangeLow=(High-Low)/Low, RangeOpen=(High-Low)/Open."""
    return (crear_return(df)
            .withColumn("RangeLow", (F.col("High") - F.col("Low")) / F.col("Low"))
            .withColumn("RangeOpen", (F.col("High") - F.col("Low")) / F.col("Open")))


def matriz_correlacion(df, columnas= COLS_CORRELACION) -> pd.DataFrame:
    """Matriz de Pearson entre las columnas indicadas (pyspark.ml.stat.Correlation)."""
    vectores = VectorAssembler(inputCols=columnas, outputCol="features").transform(df)
    matriz = Correlation.corr(vectores, "features", "pearson").head()[0].toArray()
    return pd.DataFrame(matriz, index=columnas, columns=columnas)


def correlacion_pearson(df, col_a: str, col_b: str) -> float:
    """Correlación de Pearson entre dos columnas, usando cada fila tal cual."""
    return df.stat.corr(col_a, col_b, "pearson")


def crear_anio_mes(df, col_fecha: str = "FechaKey"):
    """Extrae Anio y Mes de una clave de fecha con formato yyyymmdd (p. ej. 20241017)."""
    return (df
            .withColumn("Anio", F.floor(F.col(col_fecha) / 10000).cast("int"))
            .withColumn("Mes", (F.floor(F.col(col_fecha) / 100) % 100).cast("int")))


def agrupar_sector_mes(df, col_sector: str = "Sector"):
    """Una fila por (sector, año, mes) con RetMedioMes y SentMedioMes (medias del grupo)."""
    return (df.groupBy(col_sector, "Anio", "Mes")
              .agg(F.avg("Return").alias("RetMedioMes"),
                   F.avg("Sentimiento").alias("SentMedioMes"),
                   F.count("*").alias("n_filas"))
              .orderBy(col_sector, "Anio", "Mes"))


def preparar_derivadas(df, columnas_base):
    """Castea a double las columnas base, quita nulos y filas con Open/Low = 0 y añade
    las variables derivadas (Return, RangeLow, RangeOpen)."""
    df = (df.select(*[F.col(c).cast("double").alias(c) for c in columnas_base])
            .dropna()
            .filter((F.col("Open") > 0) & (F.col("Low") > 0)))
    return crear_variables_derivadas(df)


def perfil_clusters(predicciones, columnas, col_orden: str = "RangeOpen") -> pd.DataFrame:
    """Media de cada variable por cluster, ordenado por col_orden (menor a mayor), con una
    etiqueta: el de menor col_orden = tranquilo y el de mayor = volátil."""
    perfil = (predicciones.groupBy("prediction")
              .agg(F.count("*").alias("n_dias"), *[F.avg(c).alias(c) for c in columnas])
              .toPandas()
              .sort_values(col_orden)
              .reset_index(drop=True))
    etiquetas = ["intermedio"] * len(perfil)
    etiquetas[0] = "tranquilo"
    if len(perfil) > 1:
        etiquetas[-1] = "volátil"
    perfil["etiqueta"] = etiquetas
    return perfil