import yfinance as yf

#Ej1-a
def descargar_historico(spark, ticker, fecha_ini, fecha_fin):

    pdf = yf.Ticker(ticker).history(start=fecha_ini, end=fecha_fin, interval="1d", auto_adjust=False)
    
    if pdf.empty:
        return None
    
    pdf.reset_index(inplace=True)

    pdf["Ticker"] = ticker

    return spark.createDataFrame(pdf)
