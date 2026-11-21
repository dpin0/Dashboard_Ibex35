#vista ejercicio 5b

def mostrar_ejercicio_5b(r):
    print("Ej5-b")
    print(f"¿Sigue rechazándolo? {r['rechazado']}")
    print(f"Columnas antes:   {r['columnas_antes']}")
    print(f"Columnas después: {r['columnas_despues']}")
    print(f"Filas antes: {r['filas_antes']} | después: {r['filas_despues']}")
    print(f"Filas con Close_mas5 nulo (las antiguas): {r['nulos_close_mas5']}")
    print("\nComentario: con mergeSchema Delta ya no rechaza la escritura: "
          "evoluciona el esquema y añade Close_mas5 a la tabla. Las filas "
          "antiguas quedan con null en esa columna. Se crea una versión nueva.")