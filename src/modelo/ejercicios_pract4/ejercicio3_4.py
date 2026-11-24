#ejercicio 3 - práctica 4
#recuperar runs del proyecto

import mlflow
from src.modelo.ejercicios_pract4.config_pract4 import MLFLOW_URI

# Métrica de cada experimento y si mayor es mejor (True) o menor es mejor (False)
METRICAS = {"silhouette": True, "davies_bouldin": False}


def recuperar_runs_ordenadas() -> list:
    """Devuelve una lista de dicts {experimento, metrica, runs}, con las runs de
    cada experimento ordenadas de mejor a peor según su métrica."""
    mlflow.set_tracking_uri(MLFLOW_URI)
    resultado = []
    for exp in mlflow.search_experiments():
        runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
        if runs.empty:
            continue
        for metrica, mayor_mejor in METRICAS.items():
            col = f"metrics.{metrica}"
            if col in runs.columns and runs[col].notna().any():
                ordenadas = runs.sort_values(by=col, ascending=not mayor_mejor)
                resultado.append({"experimento": exp.name, "metrica": metrica,
                                  "runs": ordenadas})
    return resultado