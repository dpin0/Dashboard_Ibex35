#vista ejercicio 5d

def mostrar_ejercicio_5d(r):
    print("Ej5-d")
    r["historial"].select("version", "timestamp", "operation",
                          "operationParameters").show(truncate=False)
    print(f"Versión leída (antes del 5a): {r['version_antes_5a']}")
    print(f"Columnas versión antigua: {r['columnas_antigua']}")
    print(f"Columnas versión actual:  {r['columnas_actual']}")
    print(f"Filas antigua: {r['filas_antigua']} | actual: {r['filas_actual']}")
    print(f"Filas BBVA antigua: {r['bbva_antigua']} | actual: {r['bbva_actual']}")
    print(f"¿Todo igual? {r['filas_antigua'] == r['filas_actual'] and r['columnas_antigua'] == r['columnas_actual']}")
    print("Comentario: la versión antigua no tiene Close_mas5, conserva BBVA y no tiene los duplicados del 5b. "
        "versionAsOf solo la lee; la tabla actual no cambia hasta que se hace el restore.")