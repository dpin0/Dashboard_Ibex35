"""Variables derivadas y correlación de Pearson (lógica reutilizable)."""
import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
from pyspark.sql import functions as F
from src.modelo.ejercicios_pract4.config_pract4 import COLS_CORRELACION


def crear_return(df):
    """Return=(Close-Open)/Open."""
    return df.withColumn("Return", (F.col("Close") - F.col("Open")) / F.col("Open"))

def crear_variables_derivadas(df):
    """Return=(Close-Open)/Open, RangeLow=(High-Low)/Low, RangeOpen=(High-Low)/Open."""
    return (df
            .withColumn("Return", (F.col("Close") - F.col("Open")) / F.col("Open"))
            .withColumn("RangeLow", (F.col("High") - F.col("Low")) / F.col("Low"))
            .withColumn("RangeOpen", (F.col("High") - F.col("Low")) / F.col("Open")))


def matriz_correlacion(df, columnas=COLS_CORRELACION) -> pd.DataFrame:
    """Matriz de Pearson entre las columnas indicadas (pyspark.ml.stat.Correlation)."""
    vectores = VectorAssembler(inputCols=columnas, outputCol="features").transform(df)
    matriz = Correlation.corr(vectores, "features", "pearson").head()[0].toArray()
    return pd.DataFrame(matriz, index=columnas, columns=columnas)


def correlacion_pearson(df, col_a: str, col_b: str) -> float:
    """Correlación de Pearson entre dos columnas, usando cada fila tal cual."""
    return df.stat.corr(col_a, col_b, "pearson")
