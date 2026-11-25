from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.clustering import GaussianMixture
from pyspark.ml.feature import VectorAssembler, StandardScaler
from src.modelo.ejercicios_pract3.config_pract3 import SEED_MODELO, FEATURES


def construir_pipeline(k: int, seed: int = SEED_MODELO, features=FEATURES) -> Pipeline:
    ensamblador = VectorAssembler(inputCols=list(features), outputCol="features")
    escalador = StandardScaler(inputCol="features", outputCol="scaled_features",
                               withMean=True, withStd=True)
    gmm = GaussianMixture(featuresCol="scaled_features", predictionCol="prediction",
                          k=k, seed=seed)
    return Pipeline(stages=[ensamblador, escalador, gmm])


def entrenar(df, k: int, seed: int = SEED_MODELO, features=FEATURES) -> PipelineModel:
    return construir_pipeline(k, seed, features).fit(df)


def log_likelihood(modelo: PipelineModel) -> float:
    """Log-verosimilitud del modelo (mayor es mejor); solo existe en mezclas gaussianas."""
    return float(modelo.stages[-1].summary.logLikelihood)

# Modelo Gaussian Mixture: pipeline VectorAssembler -> StandardScaler -> GaussianMixture