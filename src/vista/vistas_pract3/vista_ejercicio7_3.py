#vista ejercicio 7 - práctica 3

def mostrar_ejercicio7_3(r: dict) -> None:
    print("Ej 7")
    print(f"Filas empresa-día: {r['n_filas']} | empresas: {r['n_empresas']}")
    print(f"Correlación de Pearson (Sentimiento, Return) = {r['correlacion']:.4f}")