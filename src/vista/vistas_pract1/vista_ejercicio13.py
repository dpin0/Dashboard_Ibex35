#vista ejercicio 13

def mostrar_ejercicio_13(r):
    print("Ej13")
    for nombre, n in r["filas"].items():
        print(f"{nombre:20s}: {n} filas")
    print(f"Esquema del hecho: {r['esquema_hecho']}")
    print(f"Exportado en: {r['ruta']}")