#vista ejercicio 8

def mostrar_ejercicio_8(r):
    print("=== Ejercicio 8: silver de sentimiento ===")
    print(f"Filas bronze/ibex:        {r['filas_ibex']}")
    print(f"Filas bronze/sentimiento: {r['filas_bronze']}")
    print(f"Filas silver/sentimiento: {r['filas_silver']}")
    print(f"Fechas sentimiento: {r['rango_sent'][0]} -> {r['rango_sent'][1]}")
    print(f"Fechas ibex:        {r['rango_ibex'][0].date()} -> {r['rango_ibex'][1].date()}")
    print("Filas por sector en silver:")
    for sector, n in r["por_sector"]:
        print(f"  {sector}: {n}")
    r["silver"].show(5)