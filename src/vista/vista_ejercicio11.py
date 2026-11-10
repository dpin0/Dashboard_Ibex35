#vista ejercicio 11

def mostrar_ejercicio_11(r):
    print("Ej11")
    print(f"(a) Precios sin sentimiento: {r['n_a']}")
    r["resumen_a"].show(truncate=False)
    print(f"(b) Sentimiento sin precios: {r['n_b']}")
    r["resumen_b"].show(truncate=False)
    print(f"Nulos de sentimiento antes: {r['nulos_antes']} -> después de rellenar: {r['nulos_despues']}")