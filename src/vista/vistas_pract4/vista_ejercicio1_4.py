#vista ejercicio 1 - práctica 4

def mostrar_ejercicio1_4(r: dict) -> None:
    print("Ej1")

    print(f"Run ID: {r['run_id']}")
    print(f"Número de clusters: {r['n_clusters']} (k={r['k']})")
    print(f"Silhouette = {r['silhouette']:.4f}")
    for cluster, n in r["tamanos"]:
        print(f"  Cluster {cluster}: {n} días")
