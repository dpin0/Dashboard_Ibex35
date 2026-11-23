#vista ejercicio 5 - práctica 4

def mostrar_ejercicio5_4(r: dict) -> None:
    print(f"\nEj 5: Hyperopt + MLflow con {r['empresa']}")
    print("Intentos (k, davies_bouldin):")
    for k, loss in r["intentos"]:
        print(f"  k={k}  DB={loss:.4f}")
    print(f"Mejor k para {r['empresa']}: {r['mejor_k']} (Davies-Bouldin={r['mejor_loss']:.4f})")
    print("\nExperimentos disponibles y su mejor run:")
    for e in r["experimentos"]:
        print(f"  Experimento: {e['experimento']}")
        print(f"    Run ID: {e['run_id']} | parámetros: {e['parametros']} "
              f"| {e['metrica']}: {e['valor']:.4f}")