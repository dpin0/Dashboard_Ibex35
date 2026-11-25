#ejercicio 4 - práctica 3
#crear f para guardar las features usadas con col version
#recuperar versión 1 de features, reentrenar y comprobar mismo resultado 

import numpy as np
from pyspark.sql import functions as F
from src.modelo import kmeans
from src.modelo.leer_gold import leer_tabla
from src.modelo.feature_store import guardar_features, recuperar_features
from src.modelo.ejercicios_pract3.config_pract3 import TABLA_HECHOS, VALOR_EMPRESA,FEATURES,COL_TICKER, SEED_MODELO

COL_CLAVE = "FechaKey"

def _features_con_clave(spark):
    """Features usadas en Ej1/Ej2 (Open, Close de BBVA) más la clave (Ticker, FechaKey)."""
    return (leer_tabla(spark, TABLA_HECHOS)
            .filter(F.col(COL_TICKER) == VALOR_EMPRESA)
            .select(COL_TICKER, COL_CLAVE,
                    *[F.col(c).cast("double").alias(c) for c in FEATURES])
            .dropna())


def _preparar(df):
    """Mismo orden y 1 partición: entran al algoritmo igual para no alterar la inicialización de KMeans"""
    return df.orderBy(COL_CLAVE).coalesce(1).cache()


def ejercicio4_3(spark, k: int = 3, version: int = 1) -> dict:
    # 1) Features originales y guardado de la versión 1 en el feature store
    original = _preparar(_features_con_clave(spark))
    guardar_features(original, version)

    # 2) Recuperación de esa versión concreta
    recuperado = _preparar(recuperar_features(spark, version))

    # 3) Entrenamiento con la misma seed sobre ambos datasets
    modelo_a = kmeans.entrenar(original, k, seed=SEED_MODELO)
    modelo_b = kmeans.entrenar(recuperado, k, seed=SEED_MODELO)
    pred_a = modelo_a.transform(original)
    pred_b = modelo_b.transform(recuperado)

    # 4) Comparación: centroides, silhouette y asignación de cluster fila a fila
    centros_a = np.array(modelo_a.stages[-1].clusterCenters())
    centros_b = np.array(modelo_b.stages[-1].clusterCenters())
    iguales_centros = bool(np.allclose(centros_a, centros_b))
    sil_a = kmeans.silhouette(pred_a)
    sil_b = kmeans.silhouette(pred_b)
    diferentes = (pred_a.select(COL_CLAVE, F.col("prediction").alias("pa"))
                  .join(pred_b.select(COL_CLAVE, F.col("prediction").alias("pb")), on=COL_CLAVE)
                  .filter(F.col("pa") != F.col("pb")).count())

    # POR QUÉ FAVORECE LA REPRODUCIBILIDAD:
    # Feature store congela los datos de entrada de un entrenamiento en vez de
    #recalcularlos cada vez, no pueden cambiar sin que se sepa
    # Con mismos datos + mismo código + seed fija (elimina el azar de KMeans) el resultado es idéntico
    # Por eso, cualquier modelo se puede recrear, auditar y comparar apuntando a "features versión N".
    
    return {"k": k, "version": version, "filas_original": original.count(),
            "filas_recuperadas": recuperado.count(),
            "centroides_iguales": iguales_centros,
            "silhouette_original": sil_a, "silhouette_recuperado": sil_b,
            "filas_con_cluster_distinto": diferentes,
            "reproducible": iguales_centros and diferentes == 0
                            and abs(sil_a - sil_b) < 1e-9}