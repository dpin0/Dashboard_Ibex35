import yfinance as yf
from src.modelo.SparkSession import create_spark_session
from src.modelo.Conexion import Conexion

from src.modelo.clase1.ejercicio1_a import descargar_historico
from src.modelo.clase1.ejercicio1_b import historico_ibex
from src.vista.vista_ejercicio1_a import mostrar_nulos_1a
from src.vista.vista_ejercicio1_b import mostrar_inicio_1b, mostrar_omitidos,mostrar_resultado_1b
#from src.modelo.clase1.ejercicio1_c import ejercicio1_c

'''
from src.modelo.clase1.ejercicio2_a import ejercicio2a
from src.modelo.clase1.ejercicio2_b import ejercicio2b
from src.modelo.clase1.ejercicio2_c import ejercicio2c
'''

def ControladorPrincipal():
    print(">>> Controlador iniciado")
    path = r".\lib\mssql-jdbc-13.4.0.jre11.jar"
    spark_session = create_spark_session(path)

    df = historico_ibex(spark_session)
    ejercicio1_c(df)


    print("FIN")
    spark_session.stop()


if __name__ == "__main__":
    ControladorPrincipal()

