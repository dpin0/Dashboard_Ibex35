import mlflow
import numpy as np
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from src.modelo import kmeans
from src.modelo.ejercicios_pract3.config_pract3 import MLFLOW_URI, SEED_MODELO, SEED_HYPEROPT


def buscar_mejor_k(df, experimento: str, empresa: str, k_min: int = 2, k_max: int = 8, max_evals: int = 15) -> dict:
    """Prueba k entre k_min y k_max minimizando Davies-Bouldin y registra cada intento
    como una run del experimento indicado."""
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment(experimento)
    espacio = {"k": hp.quniform("k", k_min, k_max, 1)}

    def objetivo(params):
        k = int(params["k"])
        with mlflow.start_run(run_name=f"kmeans_k{k}"):
            # SEED 1 (modelo): fija la inicialización de los centroides de KMeans en Spark;
            # mismo k + mismas features => siempre el mismo clustering.
            modelo = kmeans.entrenar(df, k, seed=SEED_MODELO)
            db = kmeans.davies_bouldin(modelo.transform(df))
            mlflow.log_param("k", k)
            mlflow.log_param("empresa", empresa)
            mlflow.log_param("seed_modelo", SEED_MODELO)
            mlflow.log_param("seed_hyperopt", SEED_HYPEROPT)
            mlflow.log_metric("davies_bouldin", db)
        return {"loss": db, "status": STATUS_OK}   # menor es mejor: se minimiza directamente

    trials = Trials()
    # SEED 42 (Hyperopt): fija (rstate) qué valores de k propone TPE en cada iteración,
    # haciendo reproducible la búsqueda (qué combinaciones se prueban y en qué orden).
    mejor = fmin(fn=objetivo, space=espacio, algo=tpe.suggest, max_evals=max_evals,
                 trials=trials, rstate=np.random.default_rng(SEED_HYPEROPT))
    return {"empresa": empresa, "mejor_k": int(mejor["k"]), "mejor_loss": min(trials.losses()),
            "intentos": [(int(t["misc"]["vals"]["k"][0]), t["result"]["loss"])
                         for t in trials.trials]}