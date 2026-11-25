#ejercicio 2 - práctica 3
#Hyperopt + MLflow => elegir mejor k (métrica = Davies-Bouldin)

from src.modelo.hyperopt import buscar_mejor_k
from src.modelo.ejercicios_pract3.config_pract3 import VALOR_EMPRESA


def ejercicio2_3(df, k_min: int = 2, k_max: int = 8, max_evals: int = 15) -> dict:
    # Las dos seeds se fijan dentro de buscar_mejor_k (busqueda_hyperopt.py):
    #  - seed=SEED_MODELO (1): fija el azar de KMeans (inicialización de centroides).
    #  - rstate=default_rng(SEED_HYPEROPT) (42): fija qué valores de k propone Hyperopt.
    return buscar_mejor_k(df, "kmeans_BBVA", VALOR_EMPRESA, k_min, k_max, max_evals)

