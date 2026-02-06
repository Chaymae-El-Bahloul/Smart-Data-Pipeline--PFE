from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from src.adaptation import choose_processing_mode

# ---------------------------------
# Spark session (une seule fois)
# ---------------------------------
spark = SparkSession.builder \
    .appName("PFE_Spark_Processing") \
    .master("local[*]") \
    .getOrCreate()


def process_with_spark(data: dict):
    """
    Traitement Spark auto-adaptatif
    """
    df = spark.createDataFrame([data])
    df.show()

    mode = choose_processing_mode(data)

    if mode == "NORMAL":
        df_processed = df \
            .withColumn("processing_mode", lit("NORMAL")) \
            .withColumn("value_processed", col("value") + 10)
    else:
        df_processed = df \
            .withColumn("processing_mode", lit("HIGH_LOAD")) \
            .withColumn("value_processed", col("value") * 2)

    print(" Résultat du traitement Spark :")
    df_processed.show()

    return df_processed

