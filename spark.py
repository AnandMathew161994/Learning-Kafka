from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum as _sum, first, last, max as _max, min as _min, expr
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType, LongType


# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("StockTickProcessor") \
    .master("spark://spark-master:7077")\
    .getOrCreate()



# 2. Define the schema
schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", DoubleType()) \
    .add("volume", IntegerType()) \
    .add("timestamp", LongType())  # epoch millis

# 3. Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:19092") \
    .option("subscribe", "stock_ticks31") \
    .option("startingOffsets", "latest") \
    .option("kafka.security.protocol", "SASL_PLAINTEXT") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.sasl.jaas.config", 
        'org.apache.kafka.common.security.plain.PlainLoginModule required '
        'username="aby" password="aby";'
    ) \
    .load()

# 4. Parse the JSON
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# 5. Add timestamp column (convert millis to timestamp)
with_ts = json_df.withColumn("event_time", (col("timestamp") / 1000).cast("timestamp"))

with_ts = json_df.withColumn("event_time", (col("timestamp") / 1000).cast("timestamp"))

#  Add watermark before aggregation
with_watermark = with_ts.withWatermark("event_time", "1 minute")

# 6Compute OHLCV + VWAP per 1-second window
agg_df = with_watermark.groupBy(
    window(col("event_time"), "1 second"),
    col("symbol")
).agg(
    first("price").alias("open"),
    _max("price").alias("high"),
    _min("price").alias("low"),
    last("price").alias("close"),
    _sum("volume").alias("volume"),
    (_sum(col("price") * col("volume")) / _sum("volume")).alias("vwap"))

# 7. Output to console (for dev)
query = agg_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
