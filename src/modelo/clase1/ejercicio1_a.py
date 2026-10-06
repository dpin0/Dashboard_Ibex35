import yfinance as yf

#Ej1-a
def descargar_historico(spark, ticker, fecha_ini, fecha_fin):

    print("Ej1-a")

    pdf = yf.Ticker(ticker).history(start=fecha_ini, end=fecha_fin, interval="1d", auto_adjust=False)
    pdf.reset_index(inplace=True)
    pdf["Ticker"] = ticker

    return spark.createDataDrame(pdf)

print("Fecha no admite nulos, ni ticker, ni dividends")
print("Volume si admite nulos")

'''
¿Open, high, low, close?
'''   