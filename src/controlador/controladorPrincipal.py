import yfinance as yf
from src.modelo.Conexion.spark_session import create_spark_session
from src.modelo.Conexion.Conexion import Conexion
from src.modelo.clase1.ejercicio1_a import ejercicio1a
from src.modelo.clase1.ejercicio1_b import ejercicio1b
from src.modelo.clase1.ejercicio1_c import ejercicio1c
from src.modelo.clase1.ejercicio2_a import ejercicio2a
from src.modelo.clase1.ejercicio2_b import ejercicio2b
from src.modelo.clase1.ejercicio2_c import ejercicio2c


def ControladorPrincipal():
    print(">>> Controlador iniciado")
    path = r".\lib\mssql-jdbc-13.4.0.jre11.jar"
    spark_session = create_spark_session(path)

    ejercicio1a(spark_session)
    ejercicio1b(spark_session)
    #ejercicio1c(spark_session)


    print("FIN")
    spark_session.stop()


if __name__ == "__main__":
    ControladorPrincipal()

