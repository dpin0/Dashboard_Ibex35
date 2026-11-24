#vista ejercicio 6 - práctica 4

def mostrar_ejercicio6_4(r: dict) -> None:
    print("Ej 6")
    print(f"Empresa: {r['empresa']} | filas usadas: {r['n_filas']}")
    print(r["matriz"].round(3).to_string())