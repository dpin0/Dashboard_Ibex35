
class Conexion:
    def __init__(self, servidor="localhost", puerto=1433, base_datos="IBEX35", usuario="sa", password="olacaracola"):
        self.url = (
            f"jdbc:sqlserver://{servidor}:{puerto};"
            f"databaseName={base_datos};"
            f"encrypt=true;trustServerCertificate=true"
        )
        self.propiedades = {
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "user": usuario,
            "password": password
        }

    def escribir_tabla(self, df, tabla, modo="overwrite"):
        df.write.jdbc(
            url=self.url,
            table=tabla,
            mode=modo,
            properties=self.propiedades
        )
        print(f"Tabla '{tabla}' guardada correctamente ({modo}).")