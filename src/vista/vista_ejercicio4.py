def mostrar_ejercicio_4(r):
    print("Ej4")
    print(f"Versión actual antes de cargar: {r['version_actual']}")
    print(r["historial_actual"][["version", "timestamp", "operation"]])
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

      #En el historial aparece la operación CONVERT y que esa versión 0 es el punto de partida del time travel.
    
    print("Comentario: ")