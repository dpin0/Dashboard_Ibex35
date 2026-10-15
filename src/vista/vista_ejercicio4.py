def mostrar_ejercicio_4(r):
    print(" Ejercicio 4: MERGE sobre (Ticker, Fecha) ===")
    print(f"Versión actual antes de cargar: {r['version_actual']}")
    print(f"Filas iniciales: {r['filas_inicial']}")
    print(f"Filas tras 1ª ejecución: {r['filas_tras_1']} "
          f"(+{r['filas_tras_1'] - r['filas_inicial']})")
    print(f"Filas tras 2ª ejecución: {r['filas_tras_2']} "
          f"(+{r['filas_tras_2'] - r['filas_tras_1']})")
    print(f"¿Sube en la 1ª? {r['filas_tras_1'] > r['filas_inicial']}")
    print(f"¿Igual en la 2ª? {r['filas_tras_2'] == r['filas_tras_1']}")

    print("\nHistorial de la tabla:")
    r["historial"].select("version", "timestamp", "operation",
                          "operationMetrics").show(truncate=False)

    print("Comentario: ")