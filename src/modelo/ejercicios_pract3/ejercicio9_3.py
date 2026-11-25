#ejercicio 9 - práctica 3

"""Ej9: clustering de días de mercado (tranquilos vs volátiles) con KMeans y Gaussian Mixture.

Selección de características a partir de la matriz del Ej6:
  - Open, High, Low, Close tienen correlación ~0,999 entre sí -> redundantes.
  - RangeLow y RangeOpen tienen correlación 0,999 -> redundantes.
  - Se conservan Return, RangeOpen, Volume y Sentimiento (la mayor correlación entre ellas
    es 0,363, entre Volume y RangeOpen), por lo que aportan información distinta.
Objetivo (A): separar días tranquilos de días volátiles. Utilidad práctica: gestión de riesgo
(reducir exposición o ajustar stop-loss en días volátiles, no operar con señales débiles
en días tranquilos, filtrar el régimen de mercado antes de aplicar una estrategia).
Métrica de calidad distinta a silhouette: Davies-Bouldin (menor es mejor)."""
import mlflow
import mlflow.spark
from src.modelo import kmeans as modelo_kmeans
from src.modelo import gaussian_mixture as modelo_gmm
from src.modelo.leer_gold import leer_tabla
from src.modelo.estadisticas import preparar_derivadas, perfil_clusters
from src.modelo.ejercicios_pract3.config_pract3 import VALOR_EMPRESA, MLFLOW_URI, TABLA_HECHOS, COL_TICKER, EXPERIMENTO_EJ9_KMEANS, COLS_BASE_CORR, EXPERIMENTO_EJ9_GMM, KS_EJ9, FEATURES_EJ9, SEED_MODELO
from pyspark.sql import functions as F


def ejercicio9_3(spark, empresa: str = VALOR_EMPRESA) -> dict:
    mlflow.set_tracking_uri(MLFLOW_URI)
    crudo = leer_tabla(spark, TABLA_HECHOS).filter(F.col(COL_TICKER) == empresa)
    df = preparar_derivadas(crudo, COLS_BASE_CORR).cache()

    algoritmos = {"kmeans": (EXPERIMENTO_EJ9_KMEANS, modelo_kmeans.entrenar),
                  "gmm": (EXPERIMENTO_EJ9_GMM, modelo_gmm.entrenar)}
    resultados, mejor = [], None
    for nombre, (experimento, entrenar) in algoritmos.items():
        mlflow.set_experiment(experimento)            # un experimento por algoritmo y dato
        for k in KS_EJ9:
            with mlflow.start_run(run_name=f"{nombre}_k{k}") as run:
                modelo = entrenar(df, k, SEED_MODELO, FEATURES_EJ9)   # seed fija
                pred = modelo.transform(df)
                db = modelo_kmeans.davies_bouldin(pred)
                mlflow.log_param("algoritmo", nombre)
                mlflow.log_param("k", k)
                mlflow.log_param("empresa", empresa)
                mlflow.log_param("seed_modelo", SEED_MODELO)
                mlflow.log_param("features", ",".join(FEATURES_EJ9))
                mlflow.log_metric("davies_bouldin", db)
                if nombre == "gmm":
                    mlflow.log_metric("log_likelihood", modelo_gmm.log_likelihood(modelo))
                mlflow.spark.log_model(modelo, "model")
            resultados.append({"algoritmo": nombre, "k": k, "davies_bouldin": db,
                               "run_id": run.info.run_id})
            if mejor is None or db < mejor["davies_bouldin"]:
                mejor = {"algoritmo": nombre, "k": k, "davies_bouldin": db, "pred": pred}

    perfil = perfil_clusters(mejor["pred"], FEATURES_EJ9)
    mejor.pop("pred")
    return {"empresa": empresa, "features": FEATURES_EJ9, "n_filas": df.count(),
            "resultados": resultados, "mejor": mejor, "perfil": perfil}