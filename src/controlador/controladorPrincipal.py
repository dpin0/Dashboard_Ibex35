import yfinance as yf
pdf = yf.Ticker("BBVA.MC").history(start="2021-10-01", end="2026-10-01",
 interval="1d", auto_adjust=False)

