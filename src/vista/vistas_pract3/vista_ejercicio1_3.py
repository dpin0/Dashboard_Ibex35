#vista ejercicio 1 - práctica 3

def mostrar_ejercicio1_3(r: dict) -> None:
    print("Ej 1")

    print("Intentos (k, silhouette):")
    for k, sil in r["intentos"]:
        print(f"  k={k}  Silhouette={sil:.4f}")
    print(f"Mejor k (mayor silhouette): k={r['k']} ({r['silhouette']:.4f})")

    print(f"Run ID: {r['run_id']}")

    print(f"Número de clusters: {r['n_clusters']} (k={r['k']})")
    print(f"Silhouette = {r['silhouette']:.4f}")
    for cluster, n in r["tamanos"]:
        print(f"  Cluster {cluster}: {n} días")