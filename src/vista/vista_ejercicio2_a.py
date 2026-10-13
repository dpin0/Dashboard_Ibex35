def mostrar_ejercicio_2a(df):
    print("Esquema del CSV de sentimiento:")
    df.printSchema()

    print("Primeras filas:")
    df.show(5, truncate=False)

    print(
        "Comentario:"
    )