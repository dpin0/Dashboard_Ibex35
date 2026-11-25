#vista ejercicio 6 - práctica 3

def mostrar_ejercicio6_3(r: dict) -> None:
    print("Ej 6")
    print(f"Empresa: {r['empresa']} | filas usadas: {r['n_filas']}")
    print(r["matriz"].round(3).to_string())