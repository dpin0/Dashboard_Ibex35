from src.modelo.SparkSession import create_spark_session

from src.modelo.ejercicios.ejercicio1_a import descargar_historico
from src.modelo.ejercicios.ejercicio1_b import historico_ibex
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

def ControladorPrincipal():
    print(">>> Controlador iniciado")
    #path = r".\lib\mssql-jdbc-13.4.0.jre11.jar"
    spark_session = create_spark_session()
    try:
        # Ejercicios 1a y 1b
        '''
        # Descomentar para ejecutar de nuevo ->
        df = historico_ibex(spark_session)
        '''
        
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
        nuevos = historico_ibex(spark_session)  
        resultados_4 = ejercicio4(spark_session, nuevos)
        mostrar_ejercicio_4(resultados_4)

        # Ejercicio 5a

        # Ejercicio 5b
        print("FIN")
        
    finally:
        spark_session.stop()


if __name__ == "__main__":
    ControladorPrincipal()

