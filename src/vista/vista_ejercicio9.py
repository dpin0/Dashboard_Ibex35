#vista ejercicio 9

def mostrar_ejercicio_9(r):
    print("Ej9")
    print(f"Filas silver/ibex: {r['filas_ibex']}")
    r["ibex"].show(5)
    print(f"Filas silver/empresas: {r['filas_empresas']}")
    r["empresas"].show(5, truncate=False)