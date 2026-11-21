#vista ejercicio 12

def mostrar_ejercicio_12(r):
    print("Ej12")
    print(f"Columnas del hecho: {r['columnas']}")
    print(f"Filas con sentimiento imputado: {r['imputadas']}")
    r["muestra"].show(5, truncate=False)