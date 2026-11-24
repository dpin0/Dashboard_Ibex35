#ejercicio 5 - práctica 4
#repetir entrenamiento MLflow + Hyperopt con otra empresa

from src.modelo.hyperopt import buscar_mejor_k
from src.modelo.leer_gold import cargar_apertura_cierre
from src.modelo.ejercicios_pract4.ejercicio3_4 import recuperar_runs_ordenadas

def mejores_runs_por_experimento() -> list:
    """Lista de experimentos disponibles con su mejor run"""
    mejores = []
    for g in recuperar_runs_ordenadas():
        mejor = g["runs"].iloc[0]       # primera fila = mejor según el sentido de la métrica
        parametros = {c.replace("params.", ""): mejor[c] for c in g["runs"].columns
                      if c.startswith("params.") and mejor[c] is not None}
        mejores.append({"experimento": g["experimento"], "metrica": g["metrica"],
                        "run_id": mejor["run_id"], "parametros": parametros,
                        "valor": mejor[f"metrics.{g['metrica']}"]})
    return mejores


def ejercicio5_4(spark) -> dict:
    df = cargar_apertura_cierre(spark, "IBE.MC").cache()
    resultado = buscar_mejor_k(df, "kmeans_IBE", "IBE.MC")
    resultado["experimentos"] = mejores_runs_por_experimento()

    # POR QUÉ SEPARAR EN EXPERIMENTOS:
    # Hay que separar experimentos por algoritmo y dato de forma que se pueda aplicar 
    #el mismo algoritmo sobre datos diferentes sin que las runs se mezclen.
    # En cada experimento se compara qué hiperparámetros van mejor;
    #entre experimentos se compara el mismos algoritmo y métrica sobre otros datos
    # Así se ve si un k sirve para cualquier empresa o depende de los datos
    return resultado