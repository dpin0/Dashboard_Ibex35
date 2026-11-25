#vista ejercicio 2 - práctica 3

def mostrar_ejercicio2_3(r: dict) -> None:
    print("Ej 2")

    print("Intentos (k, davies_bouldin):")
    for k, loss in r["intentos"]:
        print(f"  k={k}  DB={loss:.4f}")
    print(f"Número de agrupaciones seleccionado por Hyperopt: k={r['mejor_k']} "
          f"(Davies-Bouldin={r['mejor_loss']:.4f})")
