from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

spark = SparkSession.builder \
    .appName("ReadKafkaFrames") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("video_id", StringType()) \
    .add("video_name", StringType()) \
    .add("frame_number", IntegerType()) \
    .add("timestamp_sec", DoubleType()) \
    .add("fps", DoubleType()) \
    .add("format", StringType()) \
    .add("image_b64", StringType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "raw-frames") \
    .option("startingOffsets", "earliest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json_value")

parsed_df = json_df.select(
    from_json(col("json_value"), schema).alias("data")
).select("data.*")

result = parsed_df.select(
    "video_id",
    "video_name",
    "frame_number",
    "timestamp_sec",
    "format"
)

query = result.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
