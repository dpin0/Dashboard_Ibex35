import yfinance as yf


pdf = yf.Ticker("BBVA.MC").history(start="2021-10-01", end="2026-10-01",
 interval="1d", auto_adjust=False) 
#devuelve un dataframe donde el indice suele ser la fecha/h 
#las columnas son Open, High, Low, Close, Volume

df.reset_index(inplace=True) # Convertir el índice 'Date' a columna

df = spark.createDataFrame(pdf)