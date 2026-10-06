from pyspark.sql import SparkSession

def create_spark_session(path):

    spark_session = (
        SparkSession.builder
        .appName("IBEX35")
        .config('spark.driver.extraClassPath', path)
        .getOrCreate()
    )

    return spark_session