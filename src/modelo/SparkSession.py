from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

def create_spark_session(path):

    spark_session = (
        SparkSession.builder
        .appName("IBEX35")
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
            )
    )
    spark = configure_spark_with_delta_pip(spark_session).getOrCreate()
    return spark