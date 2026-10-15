


def mostrar_ejercicio_3(resultados):
    print("=== Ejercicio 3: conversión de Parquet a Delta ===")
    for nombre, (historial, contenido_log) in resultados.items():
        print(f"\n--- Tabla: {nombre} ---")
        historial.select("version", "timestamp", "operation",
                         "operationParameters").show(truncate=False)
        print("Contenido de _delta_log:")
        for fichero in contenido_log:
            print(f"  - {fichero}")

    print("\nComentario: al convertir no se ha reescrito ningún dato. Los "
          "ficheros Parquet siguen intactos y solo ha aparecido la carpeta "
          "_delta_log, que contiene el log de transacciones. Dentro hay un "
          "fichero JSON (00000000000000000000.json) que registra la operación "
          "CONVERT con la lista de ficheros Parquet que forman la tabla. "
          "Cada operación futura (append, overwrite, update...) añadirá una "
          "nueva versión al log, lo que permite ver el historial, hacer "
          "time travel y tener transacciones ACID. Es una operación de "
          "metadatos, por eso es muy rápida.")