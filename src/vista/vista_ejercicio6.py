def mostrar_ejercicio_6(r):
    print("=== Ejercicio 6: RESTORE al estado del Ej4 ===")
    print(f"Restaurado a la versión: {r['version']}")
    print(f"Filas antes: {r['filas_antes']} | después: {r['filas_despues']}")
    print(f"Filas del Ej4: {r['filas_ej4']} | ¿coinciden? {r['filas_despues'] == r['filas_ej4']}")
    print(f"Filas BBVA tras restore: {r['bbva']}")
    print(f"Columnas tras restore: {r['columnas']}")
    print(f"¿Existe Close_mas5? {'Close_mas5' in r['columnas']}")

    print("\nHistorial:")
    r["historial"].select("version", "timestamp", "operation",
                          "operationParameters").show(truncate=False)
    print("\nComentario: versionAsOf solo lee una versión antigua; "
          "restoreToVersion deja la tabla realmente como estaba. RESTORE no "
          "borra el historial: crea un commit nuevo (operación RESTORE) con "
          "el contenido de la versión indicada, y el log conserva todo.")