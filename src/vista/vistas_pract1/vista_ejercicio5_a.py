#vista ejercicio 5a

def mostrar_ejercicio_5a(r):
    print("Ej5-a")
    print(f"¿Delta lo ha rechazado? {r['rechazado']}")
    print(f"Mensaje: {r['mensaje']}")
    print(f"Versión antes: {r['version_antes']} | después: {r['version_despues']}")
    print(f"Filas antes: {r['filas_antes']} | después: {r['filas_despues']}")
    print("\nComentario: Delta aplica schema enforcement: rechaza escribir "
          "una columna que no existe en el esquema de la tabla. Al fallar, "
          "no se crea ninguna versión y la tabla queda intacta.")