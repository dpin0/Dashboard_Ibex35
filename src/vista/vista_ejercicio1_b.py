
def mostrar_inicio_1b():
    print("Ej1-b")
    print("Descargando el histórico del IBEX-35 (2024-10-01 a 2026-10-01)...")

def mostrar_omitidos(omitidos):
    if omitidos:
        print("Tickers sin datos en Yahoo, omitidos:", ", ".join(omitidos))

def mostrar_resultado_1b(df):
    print("Histórico guardado en data/lake/bronze/ibex")
    df.show(5)