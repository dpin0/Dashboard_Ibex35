import mlflow
import mlflow.spark
from src.modelo import kmeans
from src.modelo.ejercicios_pract4.config_pract4 import MLFLOW_URI, SEED_MODELO, FEATURES


def ejercicio1_4(df, ks=range(2, 9)) -> dict:
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment("kmeans_BBVA_ej1")

    intentos = []   # (k, silhouette, run_id, predicciones)
    for k in ks:
        with mlflow.start_run(run_name=f"kmeans_k{k}") as run:
            modelo = kmeans.entrenar(df, k)
            pred = modelo.transform(df)
            sil = kmeans.silhouette(pred)
            mlflow.log_param("k", k)
            mlflow.log_param("seed_modelo", SEED_MODELO)
            mlflow.log_param("features", ",".join(FEATURES))
            mlflow.log_metric("silhouette", sil)
            mlflow.spark.log_model(modelo, "model")
        intentos.append((k, sil, run.info.run_id, pred))

    # El número de agrupaciones correcto es el k con mayor silhouette
    k_mejor, sil_mejor, run_mejor, pred_mejor = max(intentos, key=lambda t: t[1])
    tamanos = pred_mejor.groupBy("prediction").count().orderBy("prediction").collect()
    return {"run_id": run_mejor, "k": k_mejor, "silhouette": sil_mejor,
            "n_clusters": kmeans.numero_clusters(pred_mejor),
            "tamanos": [(r["prediction"], r["count"]) for r in tamanos],
            "intentos": [(k, s) for k, s, _, _ in intentos]}

# Pipeline (VectorAssembler + KMeans) con MLflow. Sin Hyperopt: se prueban varios k y se elige el de mayor silhouette