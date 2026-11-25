#vista ejercicio 4 - páctica 3

def mostrar_ejercicio4_3(r: dict) -> None:
    print(f"\nEj 4: Feature store (versión {r['version']})")
    print(f"Filas guardadas: {r['filas_original']} | filas recuperadas: {r['filas_recuperadas']}")
    print(f"Silhouette original:   {r['silhouette_original']:.6f}")
    print(f"Silhouette recuperado: {r['silhouette_recuperado']:.6f}")
    print(f"Centroides idénticos: {r['centroides_iguales']}")
    print(f"Filas con cluster distinto: {r['filas_con_cluster_distinto']}")
    print("REPRODUCIBLE: SÍ, mismo resultado" if r["reproducible"]
          else "REPRODUCIBLE: NO, hay diferencias")