def mostrar_ejercicio_5d(r):
    print("=== Ejercicio 5d: history() y versionAsOf ===")
    r["historial"].select("version", "timestamp", "operation",
                          "operationParameters").show(truncate=False)
    print(f"Versión leída (antes del 5a): {r['version_antes_5a']}")
    print(f"Columnas versión antigua: {r['columnas_antigua']}")
    print(f"Columnas versión actual:  {r['columnas_actual']}")
    print(f"Filas antigua: {r['filas_antigua']} | actual: {r['filas_actual']}")
    print(f"Filas BBVA antigua: {r['bbva_antigua']} | actual: {r['bbva_actual']}")
    print(f"¿Todo igual? {r['filas_antigua'] == r['filas_actual'] and r['columnas_antigua'] == r['columnas_actual']}")
    print("\nComentario: no está todo igual. La versión antigua no tiene la "
          "columna Close_mas5, conserva las filas de BBVA y no tiene las "
          "filas duplicadas del 5b. El time travel demuestra que el dato "
          "sigue recuperable, pero la tabla actual no ha cambiado.")