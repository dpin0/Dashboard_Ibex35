"""Ej4: guardar versión 1 de las features, recuperarla, reentrenar y comprobar que el
resultado es idéntico gracias a la seed fija."""
import numpy as np
from pyspark.sql import functions as F
from src.modelo import kmeans
from src.modelo.leer_gold import leer_tabla
from src.modelo.features_logica import guardar_features, recuperar_features
from src.modelo.ejercicios_pract4 import config_pract4 as cfg

COL_CLAVE = "FechaKey"


def _features_con_clave(spark):
    """Features usadas en Ej1/Ej2 (Open, Close de BBVA) más la clave (Ticker, FechaKey)."""
    return (leer_tabla(spark, cfg.TABLA_HECHOS)
            .filter(F.col(cfg.COL_TICKER) == cfg.VALOR_EMPRESA)
            .select(cfg.COL_TICKER, COL_CLAVE,
                    *[F.col(c).cast("double").alias(c) for c in cfg.FEATURES])
            .dropna())


def _preparar(df):
    """Mismo orden y una sola partición: así original y recuperado entran al algoritmo
    exactamente igual (el orden/partición podría alterar la inicialización de KMeans)."""
    return df.orderBy(COL_CLAVE).coalesce(1).cache()


def ejercicio4_4(spark, k: int = 3, version: int = 1) -> dict:
    # 1) Features originales y guardado de la versión 1 en el feature store
    original = _preparar(_features_con_clave(spark))
    guardar_features(original, version)

    # 2) Recuperación de esa versión concreta
    recuperado = _preparar(recuperar_features(spark, version))

    # 3) Entrenamiento con la misma seed sobre ambos datasets
    modelo_a = kmeans.entrenar(original, k, seed=cfg.SEED_MODELO)
    modelo_b = kmeans.entrenar(recuperado, k, seed=cfg.SEED_MODELO)
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
    # El feature store congela los datos de entrada de un entrenamiento (versión 1) en
    # lugar de recalcularlos cada vez, de modo que no pueden cambiar sin que lo
    # sepamos (nuevo código de limpieza, nuevos datos en gold...). Con los mismos
    # datos + el mismo código + la seed fija (que elimina el azar de KMeans) el
    # resultado es idéntico, y por eso cualquier modelo se puede recrear, auditar y
    # comparar en el futuro apuntando a "features versión N".
    return {"k": k, "version": version, "filas_original": original.count(),
            "filas_recuperadas": recuperado.count(),
            "centroides_iguales": iguales_centros,
            "silhouette_original": sil_a, "silhouette_recuperado": sil_b,
            "filas_con_cluster_distinto": diferentes,
            "reproducible": iguales_centros and diferentes == 0
                            and abs(sil_a - sil_b) < 1e-9}