"""Funciones reutilizables (modelo) para las Clases 3: silver, gold y export.

Cada funcion resuelve un unico problema y se reutiliza en varios ejercicios.
"""
import json

from delta.tables import DeltaTable
from pyspark.sql import functions as F, Window

RUTA_CSV_SENTIMIENTO = "data/sentimiento_ibex.csv"

RUTA_BRONZE_IBEX = "data/lake/bronze/ibex"
RUTA_BRONZE_SENTIMIENTO = "data/lake/bronze/sentimiento"
RUTA_BRONZE_EMPRESAS = "data/lake/bronze/empresas"

RUTA_SILVER_IBEX = "data/lake/silver/ibex"
RUTA_SILVER_SENTIMIENTO = "data/lake/silver/sentimiento"
RUTA_SILVER_EMPRESAS = "data/lake/silver/empresas"

RUTA_GOLD = "data/lake/gold"
RUTA_GOLD_HECHO = f"{RUTA_GOLD}/fact_cotizaciones"
RUTA_GOLD_DIM_EMPRESA = f"{RUTA_GOLD}/dim_empresa"
RUTA_GOLD_DIM_FECHA = f"{RUTA_GOLD}/dim_fecha"

RUTA_EXPORT = "data/export/gold"

# Sectores del CSV que esten en español (claves en minuscula) -> nombre de Yahoo.
# Los que ya vienen en ingles ("financial services", "utilities"...) solo se
# normalizan a Title Case. Añade aqui los que veas en tu CSV.

MAPA_SECTORES = {
    "finanzas": "Financial Services",
    "banca": "Financial Services",
    "energía": "Energy",
    "telecomunicaciones": "Communication Services",
    "turismo": "Consumer Cyclical",
    "inmobiliario": "Real Estate",
    "tecnología": "Technology",
    "salud": "Healthcare",
    "industria": "Industrials",
    "consumo": "Consumer Cyclical",
    "servicios públicos": "Utilities",
}

# Uso de IA: Claude Sonnet 5.5. Pedí ayuda para añadir limpiar_sentimiento, sentimiento_por_sector_dia y calendario_continuo, y para revisar el resto de funciones del módulo.

def leer_delta(spark, ruta):
    return spark.read.format("delta").load(ruta)


def escribir_delta(df, ruta, modo="overwrite"):
    (df.write.format("delta").mode(modo)
        .option("overwriteSchema", "true").save(ruta))


def contar_filas(spark, ruta):
    return leer_delta(spark, ruta).count()


def version_actual(spark, ruta):
    """Numero entero de la version actual de la tabla Delta."""
    return (DeltaTable.forPath(spark, ruta).history(1).select("version").collect()[0][0])


def merge_nuevos(spark, nuevos, ruta):
    """Inserta solo las filas cuya clave (Ticker, Date) no existe aun."""
    destino = DeltaTable.forPath(spark, ruta)
    (destino.alias("d")
        .merge(nuevos.alias("n"),
               "d.Ticker = n.Ticker AND d.Date = n.Date")
        .whenNotMatchedInsertAll()
        .execute())
    return contar_filas(spark, ruta)

def resumen_total(df):
    return (df.groupBy("Sector")
              .agg(F.count("*").alias("filas"),
                   F.min("Fecha").alias("desde"),
                   F.max("Fecha").alias("hasta"))
              .orderBy("Sector"))
    
# silver: sentimiento
def leer_csv_sentimiento(spark, ruta=RUTA_CSV_SENTIMIENTO):
    # Prueba ";", tabulador y ","; se queda con el primero que separe columnas.
    # Si las tildes salen rotas, añade .option("encoding", "ISO-8859-1")
    for sep in (";", "	", ","):
        df = spark.read.option("header", True).option("sep", sep).csv(ruta)
        if len(df.columns) > 1:
            return df
    return df


def limpiar_decimales(df, columnas):
    """Coma -> punto y a double. Lo no numerico queda en null (try_cast)."""
    for c in columnas:
        df = df.withColumn(
            c, F.regexp_replace(F.trim(F.col(c)), ",", ".").try_cast("double"))
    return df


def limpiar_fecha(df, columna="Fecha"):
    """Texto a date aceptando yyyy-MM-dd o d/M/yyyy (null si no encaja)."""
    f = F.coalesce(
        F.try_to_timestamp(F.col(columna), F.lit("yyyy-MM-dd")),
        F.try_to_timestamp(F.col(columna), F.lit("d/M/yyyy")))
    return df.withColumn(columna, f.cast("date"))


def a_formato_largo(df, ids, valores, col_variable, col_valor):
    """Unpivot: de formato ancho a largo."""
    return df.unpivot(ids, valores, col_variable, col_valor)


def traducir_sectores(df, mapa=MAPA_SECTORES):
    """Minusculas -> español a ingles -> Title Case (como Yahoo)."""
    df = df.withColumn("Sector", F.lower(F.trim(F.col("Sector"))))
    df = df.replace(mapa, subset=["Sector"])
    return df.withColumn("Sector", F.initcap("Sector"))

def limpiar_sentimiento(df):
    """Silver del sentimiento: ancho->largo si hace falta, fecha y decimales
    tipados, sectores traducidos, rango 0-100 y sin duplicados."""
    if "Sector" not in df.columns:      # CSV en formato ancho (una columna por sector)
        df = a_formato_largo(df, ["Fecha"], None, "Sector", "Sentimiento")
    df = limpiar_fecha(df, "Fecha")
    df = limpiar_decimales(df, ["Sentimiento"])
    df = traducir_sectores(df)
    return (df.dropna(subset=["Fecha", "Sector", "Sentimiento"])
              .filter(F.col("Sentimiento").between(0, 100))
              .dropDuplicates(["Fecha", "Sector"]))

# ------------------------------------------------------------ silver: precios
def limpiar_precios(df):
    """Date (timestamp) -> Fecha (date), tipos, nulos y duplicados."""
    df = (df.withColumn("Fecha", F.to_date("Date"))
            .withColumnRenamed("Stock Splits", "Stock_Splits"))
    for c in ["Open", "High", "Low", "Close", "Dividends", "Stock_Splits"]:
        df = df.withColumn(c, F.col(c).cast("double"))
    df = df.withColumn("Volume", F.col("Volume").cast("long"))
    columnas = ["Ticker", "Fecha", "Open", "High", "Low", "Close",
                "Volume", "Dividends", "Stock_Splits"]
    return (df.select(*columnas)
              .dropna(subset=["Ticker", "Fecha", "Close"])
              .dropDuplicates(["Ticker", "Fecha"]))


# ----------------------------------------------------------- empresas (Yahoo)
def descargar_info_empresas(spark, tickers):
    """Info cruda de Yahoo: una fila por ticker con el JSON completo."""
    import yfinance as yf
    filas = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
        except Exception:
            info = {}
        filas.append((t, json.dumps(info, default=str)))
    return spark.createDataFrame(filas, ["Ticker", "info_json"])


def empresas_silver(df_crudo):
    def campo(nombre):
        return F.get_json_object("info_json", f"$.{nombre}")
    return (df_crudo.select(
                "Ticker",
                campo("longName").alias("Nombre"),
                campo("sector").alias("Sector"),
                campo("industry").alias("Industria"),
                campo("marketCap").try_cast("long").alias("Capitalizacion"),
                campo("recommendationKey").alias("Recomendacion"))
            .dropDuplicates(["Ticker"]))


def historial(spark, ruta):
    return DeltaTable.forPath(spark, ruta).history()

    
# ------------------------------------------------------------------- gold
def precios_con_sector(precios, empresas):
    return precios.join(empresas.select("Ticker", "Sector"), "Ticker", "left")


def anti_join(izq, der, claves):
    return izq.join(der, on=claves, how="left_anti")


def clave_fecha(df):
    """Fecha como entero yyyyMMdd (clave ligera para Power BI)."""
    return df.withColumn("FechaKey",
                         F.date_format("Fecha", "yyyyMMdd").cast("int"))

def sentimiento_por_sector_dia(df):
    """Una fila por (Sector, Fecha). Evita que el left join con los precios
    multiplique filas si hubiera varios valores el mismo dia."""
    return (df.groupBy("Sector", "Fecha")
              .agg(F.round(F.avg("Sentimiento"), 2).alias("Sentimiento")))


def calendario_continuo(df, columna="Fecha"):
    """Un registro por dia natural entre la primera y la ultima fecha de df
    (incluye fines de semana y festivos: DAX lo exige para time intelligence)."""
    return (df.agg(F.min(columna).alias("a"), F.max(columna).alias("b"))
              .select(F.explode(F.sequence("a", "b", F.expr("interval 1 day")))
                       .alias("Fecha")))

def construir_dim_fecha(precios):
    fechas = clave_fecha(precios.select("Fecha").distinct())
    return fechas.select("FechaKey", "Fecha",
                         F.year("Fecha").alias("Anio"),
                         F.quarter("Fecha").alias("Trimestre"),
                         F.month("Fecha").alias("Mes"),
                         F.dayofmonth("Fecha").alias("Dia"),
                         F.dayofweek("Fecha").alias("DiaSemana"))


def construir_hecho(precios, empresas, sentimiento):
    """Hecho: solo claves (Ticker, FechaKey) y medidas. Left join: no se
    pierde ningun precio aunque no tenga sentimiento."""
    return (precios_con_sector(precios, empresas)
            .join(sentimiento, ["Sector", "Fecha"], "left")
            .transform(clave_fecha)
            .select("Ticker", "FechaKey", "Open", "High", "Low", "Close",
                    "Volume", "Dividends", "Stock_Splits", "Sentimiento"))


def anadir_calculos(df):
    """Variacion diaria, variacion % y media movil de 7 sesiones."""
    w = Window.partitionBy("Ticker").orderBy("FechaKey")
    anterior = F.lag("Close").over(w)
    return (df
            .withColumn("Var_diaria", F.col("Close") - anterior)
            .withColumn("Var_pct",
                        F.try_divide(F.col("Close") - anterior, anterior) * 100)
            .withColumn("Media_movil_7",
                        F.avg("Close").over(w.rowsBetween(-6, 0))))


def rellenar_sentimiento(df):
    """Arrastra el ultimo sentimiento conocido por ticker."""
    w = (Window.partitionBy("Ticker").orderBy("FechaKey")
         .rowsBetween(Window.unboundedPreceding, 0))
    return df.withColumn("Sentimiento",
                         F.last("Sentimiento", ignorenulls=True).over(w))


# ----------------------------------------------------------------- export
def exportar_parquet(df, ruta):
    df.coalesce(1).write.mode("overwrite").parquet(ruta)
