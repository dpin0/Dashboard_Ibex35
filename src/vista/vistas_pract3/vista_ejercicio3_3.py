#vista ejercicio 3 - práctica 3

def mostrar_ejercicio3_3(grupos: list) -> None:
    print("Ej 3")

    if not grupos:
        print("No hay runs registradas todavía.")
    for g in grupos:
        metrica = g["metrica"]
        print(f"\nExperimento: {g['experimento']}  (ordenado por {metrica})")
        for _, fila in g["runs"].iterrows():
            parametros = {c.replace("params.", ""): fila[c]
                          for c in g["runs"].columns
                          if c.startswith("params.") and fila[c] is not None}
            print(f"  Run ID: {fila['run_id']} | parámetros: {parametros} "
                  f"| {metrica}: {fila[f'metrics.{metrica}']:.4f}")