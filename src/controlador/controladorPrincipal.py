from src.modelo.SparkSession import create_spark_session

from src.modelo.ejercicios.ejercicio1_a import descargar_historico
from src.modelo.ejercicios.ejercicio1_b import historico_ibex, descargar_ibex
from src.vista.vista_ejercicio1_a import admite_nulos_1a
from src.vista.vista_ejercicio1_b import mostrar_inicio_1b, mostrar_omitidos,mostrar_resultado_1b
from src.modelo.ejercicios.ejercicio1_c import leer_1c
from src.vista.vista_ejercicio1_c import mostrar_ejercicio_1c


from src.modelo.ejercicios.ejercicio2_a import ejercicio2a
from src.modelo.ejercicios.ejercicio2_b import ejercicio2b, RUTA_BRONZE_SENTIMIENTO
from src.vista.vista_ejercicio2_a import mostrar_ejercicio_2a
from src.vista.vista_ejercicio2_b import mostrar_ejercicio_2b
from src.modelo.ejercicios.ejercicio2_c import ejercicio2c
from src.vista.vista_ejercicio2_c import mostrar_ejercicio_2c

from src.modelo.ejercicios.ejercicio3 import ejercicio3
from src.vista.vista_ejercicio3 import mostrar_ejercicio_3
from src.modelo.ejercicios.ejercicio4 import ejercicio4
from src.vista.vista_ejercicio4 import mostrar_ejercicio_4

from src.modelo.ejercicios.ejercicio5_a import ejercicio5a
from src.modelo.ejercicios.ejercicio5_b import ejercicio5b
from src.modelo.ejercicios.ejercicio5_c import ejercicio5c
from src.modelo.ejercicios.ejercicio5_d import ejercicio5d
from src.modelo.ejercicios.ejercicio6 import ejercicio6
from src.modelo.ejercicios.ejercicio8 import ejercicio8

from src.vista.vista_ejercicio5_a import mostrar_ejercicio_5a
from src.vista.vista_ejercicio5_b import mostrar_ejercicio_5b
from src.vista.vista_ejercicio5_c import mostrar_ejercicio_5c
from src.vista.vista_ejercicio5_d import mostrar_ejercicio_5d
from src.vista.vista_ejercicio6 import mostrar_ejercicio_6
from src.vista.vista_ejercicio8 import mostrar_ejercicio_8

def ControladorPrincipal():
    print(">>> Controlador iniciado")
    #path = r".\lib\mssql-jdbc-13.4.0.jre11.jar"
    spark_session = create_spark_session()
    try:
        '''
        # Ejercicios 1a y 1b
        
        # Descomentar para ejecutar de nuevo ->
        historico_ibex(spark_session)
        
        
        # Ejercicio 1c
        df_completo, df_det = leer_1c(spark_session)
        mostrar_ejercicio_1c(df_completo, df_det)

        # Ejercicio 2a
        df_sentimiento = ejercicio2a(spark_session)
        mostrar_ejercicio_2a(df_sentimiento)

        # Ejercicio 2b
        n_filas = ejercicio2b(df_sentimiento)
        mostrar_ejercicio_2b(n_filas, RUTA_BRONZE_SENTIMIENTO)

        # Ejercicio 2c
        antes, despues = ejercicio2c(spark_session, df_sentimiento)
        mostrar_ejercicio_2c(antes, despues)

        # Ejercicio 3
        resultados_3 = ejercicio3(spark_session)
        mostrar_ejercicio_3(resultados_3)

        # Ejercicio 4
        nuevos = descargar_ibex(spark_session, "2026-10-02", "2026-11-11")
        resultados_4 = ejercicio4(spark_session, nuevos)
        mostrar_ejercicio_4(resultados_4)
        
        # Ejercicio 5a
        resultados_5a = ejercicio5a(spark_session)
        mostrar_ejercicio_5a(resultados_5a)
        
        # Ejercicio 5b
        resultados_5b = ejercicio5b(spark_session)
        mostrar_ejercicio_5b(resultados_5b)
        
        # Ejercicio 5c
        resultados_5c = ejercicio5c(spark_session)
        mostrar_ejercicio_5c(resultados_5c)

        # Ejercicio 5d
        resultados_5d = ejercicio5d(spark_session, resultados_5a["version_antes"])
        mostrar_ejercicio_5d(resultados_5d)

        # Ejercicio 6
        resultados_6  = ejercicio6(spark_session, resultados_4["version_tras_1"], resultados_4["filas_tras_1"])
        mostrar_ejercicio_6(resultados_6)
        '''


        # Ejercicio 8 
        resultados_8 = ejercicio8(spark_session)
        mostrar_ejercicio_8(resultados_8)


        
        print("FIN")
        
    finally:
        spark_session.stop()


if __name__ == "__main__":
    ControladorPrincipal()

