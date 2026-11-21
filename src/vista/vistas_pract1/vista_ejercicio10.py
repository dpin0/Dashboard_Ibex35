#vista ejercicio 10

def mostrar_ejercicio_10(r):
    print("Ej10")
    print(f"Filas silver/ibex : {r['filas_silver']}")
    print(f"Filas fact_cotizaciones: {r['filas_hecho']}")
    print(f"Filas dim_empresa : {r['filas_dim_empresa']}")
    print(f"Filas dim_fecha : {r['filas_dim_fecha']}")
    print(f"Claves duplicadas : {r['claves_duplicadas']}")
    print(f"Huérfanos empresa : {r['huerfanos_empresa']}")
    print(f"Huérfanos fecha : {r['huerfanos_fecha']}")
    print(f"Filas sin sentimiento : {r['sin_sentimiento']}")
    print(f"Guardado en : {r['ruta']}")
    r["muestra"].show(5, truncate=False)