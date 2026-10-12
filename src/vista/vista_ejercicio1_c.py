def mostrar_ejercicio_1c(df, df_det):
    print("Esquema del Parquet:")
    df.printSchema()

    print("Primeras 5 filas:")
    df.show(5, truncate=False)

    print("Columnas determinadas:")
    df_det.show(5, truncate=False)

    print(
        "Ventaja de leer solo unas columnas determinadas frente a todo el DataFrame:"
    )