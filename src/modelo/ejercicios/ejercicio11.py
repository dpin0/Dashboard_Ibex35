from src.modelo.funciones_delta import (
    RUTA_SILVER_IBEX, RUTA_SILVER_EMPRESAS, RUTA_SILVER_SENTIMIENTO,
    leer_delta, anti_join, precios_con_sector, rellenar_sentimiento,
    construir_hecho, resumen_total, sentimiento_por_sector_dia
)

def ejercicio11(spark):
    precios = leer_delta(spark, RUTA_SILVER_IBEX)
    empresas = leer_delta(spark, RUTA_SILVER_EMPRESAS)
    sent = sentimiento_por_sector_dia(leer_delta(spark, RUTA_SILVER_SENTIMIENTO))

    p = precios_con_sector(precios, empresas)

    # (a) precios sin sentimiento y (b) sentimiento sin precios
    precios_sin_sent = anti_join(p, sent, ["Sector", "Fecha"])
    sent_sin_precios = anti_join(sent, p.select("Sector", "Fecha").distinct(),
                                 ["Sector", "Fecha"])

    #Sol: arrastrar el último sentimiento conocido del ticker
    hecho = construir_hecho(precios, empresas, sent)
    nulos_antes = hecho.filter(F.col("Sentimiento").isNull()).count()
    nulos_despues = (rellenar_sentimiento(hecho)
                     .filter(F.col("Sentimiento").isNull()).count())

    return {
        "n_a": precios_sin_sent.count(),
        "resumen_a": resumen_total(precios_sin_sent),
        "n_b": sent_sin_precios.count(),
        "resumen_b": resumen_total(sent_sin_precios),
        "nulos_antes": nulos_antes,
        "nulos_despues": nulos_despues,
    }