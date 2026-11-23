from src.modelo.hyperopt import buscar_mejor_k
from src.modelo.leer_gold import cargar_apertura_cierre
from src.modelo.ejercicios_pract4.ejercicio3_4 import recuperar_runs_ordenadas

EMPRESA_EJ5 = "IBE.MC"            # Iberdrola (otra empresa de la gold)
EXPERIMENTO_EJ5 = "kmeans_IBE"    # experimento distinto al de BBVA (kmeans_BBVA)


def mejores_runs_por_experimento() -> list:
    """Lista de experimentos disponibles con su mejor run (reutiliza el orden del Ej3)."""
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
    df = cargar_apertura_cierre(spark, EMPRESA_EJ5).cache()
    resultado = buscar_mejor_k(df, EXPERIMENTO_EJ5, EMPRESA_EJ5)
    resultado["experimentos"] = mejores_runs_por_experimento()

    # POR QUÉ SEPARAR EN EXPERIMENTOS:
    # Cada experimento agrupa las runs de un mismo algoritmo sobre un mismo dato
    # (kmeans_BBVA, kmeans_IBE). Dentro de uno se compara qué hiperparámetros van mejor;
    # entre experimentos se compara el mismo algoritmo y la misma métrica sobre datos
    # distintos (p. ej. el mejor k y el Davies-Bouldin de BBVA frente a los de Iberdrola)
    # sin que las runs se mezclen. Así se ve si un k sirve para cualquier empresa o
    # depende de los datos, y cada historial queda ordenado y reproducible.
    return resultado

# repetir MLflow + Hyperopt con otra empresa, en exp distinto, y listar los exp con su mejor run