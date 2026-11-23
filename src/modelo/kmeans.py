import numpy as np
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import VectorAssembler, StandardScaler
from src.modelo.ejercicios_pract4 import config_pract4 as cfg


def construir_pipeline(k: int, seed: int = cfg.SEED_MODELO) -> Pipeline:
    ensamblador = VectorAssembler(inputCols=cfg.FEATURES, outputCol="features")
    escalador = StandardScaler(inputCol="features", outputCol="scaled_features", withMean=True, withStd=True)
    kmeans = KMeans(featuresCol="scaled_features", predictionCol="prediction", k=k, seed=seed)
    return Pipeline(stages=[ensamblador, escalador, kmeans])


def entrenar(df, k: int, seed: int = cfg.SEED_MODELO) -> PipelineModel:
    return construir_pipeline(k, seed).fit(df)


def silhouette(predicciones) -> float:
    """Métrica Ej1: mayor es mejor."""
    return ClusteringEvaluator(featuresCol="scaled_features", predictionCol="prediction", metricName="silhouette").evaluate(predicciones)


def davies_bouldin(predicciones) -> float:
    """Métrica Ej2: menor es mejor (Spark no la incluye, se calcula con numpy)."""
    pdf = predicciones.select("scaled_features", "prediction").toPandas()
    X = np.vstack(pdf["scaled_features"].apply(lambda v: v.toArray()).values)
    etiquetas = pdf["prediction"].values
    ids = np.unique(etiquetas)
    if len(ids) < 2:
        return float("inf")
    centroides = np.array([X[etiquetas == c].mean(axis=0) for c in ids])
    dispersion = np.array([np.linalg.norm(X[etiquetas == c] - centroides[i], axis=1).mean()
                           for i, c in enumerate(ids)])
    total = 0.0
    for i in range(len(ids)):
        total += max((dispersion[i] + dispersion[j]) / np.linalg.norm(centroides[i] - centroides[j])
                     for j in range(len(ids)) if j != i)
    return float(total / len(ids))


def numero_clusters(predicciones) -> int:
    return predicciones.select("prediction").distinct().count()

# Modelo KMeans: pipeline VectorAssembler -> StandardScaler -> KMeans y métricas