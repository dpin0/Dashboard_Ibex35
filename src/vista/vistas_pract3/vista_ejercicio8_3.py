#vista ejercicio 8 - práctica 3

def mostrar_ejercicio8_3(r: dict, filas: int = 15) -> None:
    print("Ej 8")
    print(f"Filas empresa-día: {r['n_filas']} | grupos (sector, mes): {r['n_grupos']}")
    print(f"Primeras {filas} filas de la tabla:")
    print(r["tabla"].head(filas).round(4).to_string(index=False))
    print(f"\nCorrelación de Pearson (SentMedioMes, RetMedioMes) = {r['correlacion']:.4f}")