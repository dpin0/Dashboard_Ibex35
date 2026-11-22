import mlflow
import mlflow.spark
from src.modelo import kmeans
from src.modelo.ejercicios_pract4 import config_pract4 as cfg


def ejercicio1_4(df, k: int = 3) -> dict:
    
    mlflow.set_tracking_uri(cfg.MLFLOW_URI)
    mlflow.set_experiment(cfg.EXPERIMENTO_EJ1)
    with mlflow.start_run(run_name=f"kmeans_k{k}") as run:
        modelo = kmeans.entrenar(df, k)
        pred = modelo.transform(df)
        sil = kmeans.silhouette(pred)
        mlflow.log_param("k", k)
        mlflow.log_param("seed_modelo", cfg.SEED_MODELO)
        mlflow.log_param("features", ",".join(cfg.FEATURES))
        mlflow.log_metric("silhouette", sil)
        mlflow.spark.log_model(modelo, "model")
    tamanos = pred.groupBy("prediction").count().orderBy("prediction").collect()
    return {"run_id": run.info.run_id, "k": k, "silhouette": sil,
            "n_clusters": kmeans.numero_clusters(pred),
            "tamanos": [(r["prediction"], r["count"]) for r in tamanos]}