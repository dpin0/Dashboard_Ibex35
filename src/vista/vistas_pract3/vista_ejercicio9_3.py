#vista ejercicio 9 - práctica 3

def mostrar_ejercicio9_3(r: dict) -> None:
    print("Ej 9: Días tranquilos vs volátiles (KMeans y Gaussian Mixture)")
    print(f"Empresa: {r['empresa']} | filas: {r['n_filas']} | características: {r['features']}")
    print("\nCalidad de cada agrupación (Davies-Bouldin, menor es mejor):")
    for x in r["resultados"]:
        print(f"  {x['algoritmo']:<7} k={x['k']}  DB={x['davies_bouldin']:.4f}")
    m = r["mejor"]
    print(f"\nMejor configuración: {m['algoritmo']} con k={m['k']} (DB={m['davies_bouldin']:.4f})")
    print("\nPerfil de cada cluster (media de cada variable):")
    print(r["perfil"].round(4).to_string(index=False))