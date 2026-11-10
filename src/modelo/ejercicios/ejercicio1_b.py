import yfinance as yf
from pyspark.sql.functions import *
from src.modelo.ejercicios.ejercicio1_a import descargar_historico


#Ej1-b

# Uso de IA: Claude Sonnet 5.5. Pedi la lista de Tickers de las empresas para recorrerlas de cara a descargar su histórico
TICKERS = [
    "ACS.MC", "ACX.MC", "AENA.MC", "AMS.MC", "ANA.MC", "ANE.MC", "BBVA.MC",
    "BKT.MC", "CABK.MC", "CLNX.MC", "COL.MC", "ELE.MC", "ENG.MC", "FDR.MC",
    "FER.MC", "GRF.MC", "IAG.MC", "IBE.MC", "IDR.MC", "ITX.MC", "LOG.MC",
    "MAP.MC", "MRL.MC", "MTS.MC", "NTGY.MC", "PUIG.MC", "RED.MC", "REP.MC",
    "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC", "SLR.MC", "TEF.MC", "UNI.MC",
]

def descargar_ibex(spark, inicio, fin):
    df_unidos = None
    for t in TICKERS:
        df = descargar_historico(spark, t, inicio, fin)
        if df is None:
            continue
        df_unidos = df if df_unidos is None else df_unidos.union(df)
    return df_unidos


def historico_ibex(spark):
    df = descargar_ibex(spark, "2024-10-01", "2026-10-02").repartition(4)
    df.write.mode("overwrite").parquet("data/lake/bronze/ibex")
    return df