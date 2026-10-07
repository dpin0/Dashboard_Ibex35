import yfinance as yf
from pyspark.sql.functions import *
from src.modelo.clase1.ejercicio1_a import descargar_historico


#Ej1-b

# Uso de IA: Claude. Lista de Tickers de las empresas para recorrerlas de cara a descargar su histórico
TICKERS = [
    "ACS.MC", "ACX.MC", "AENA.MC", "AMS.MC", "ANA.MC", "ANE.MC", "BBVA.MC",
    "BKT.MC", "CABK.MC", "CLNX.MC", "COL.MC", "ELE.MC", "ENG.MC", "FDR.MC",
    "FER.MC", "GRF.MC", "IAG.MC", "IBE.MC", "IDR.MC", "ITX.MC", "LOG.MC",
    "MAP.MC", "MRL.MC", "MTS.MC", "NTGY.MC", "PUIG.MC", "RED.MC", "REP.MC",
    "ROVI.MC", "SAB.MC", "SAN.MC", "SCYR.MC", "SLR.MC", "TEF.MC", "UNI.MC",
]

def historico_ibex(spark):

    print("Ej1-b")

    df_unidos = None

    for i in TICKERS:
        df = descargar_historico(spark, i, "2024-10-01", "2026-10-02")
        if df is None:
            continue
        if df_unidos is None:
            df_unidos = df
        else:
            df_unidos = df_unidos.union(df)
        
    df_unidos.write.mode("overwrite").parquet("data/lake/bronze/ibex")
    return df_unidos
