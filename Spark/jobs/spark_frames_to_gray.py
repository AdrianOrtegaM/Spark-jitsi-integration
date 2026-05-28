from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType, BinaryType
import os

KAFKA_BOOTSTRAP = "kafka:29092"
TOPIC = "raw-frames"

OUTPUT_DIR = "/images/output_kafka_gray"
CHECKPOINT_DIR = "/images/checkpoint_kafka_gray"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

spark = SparkSession.builder.appName("KafkaFramesToGray").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("video_id", StringType()) \
    .add("video_name", StringType()) \
    .add("frame_number", IntegerType()) \
    .add("timestamp_sec", DoubleType()) \
    .add("fps", DoubleType()) \
    .add("format", StringType()) \
    .add("image_b64", StringType())

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)

json_df = df.selectExpr("CAST(value AS STRING) as json_value")

parsed_df = json_df.select(
    from_json(col("json_value"), schema).alias("data")
).select("data.*")


def save_partition(rows_iter, batch_id):
    import os
    import base64
    import numpy as np
    import cv2

    for row in rows_iter:
        video_id = row["video_id"]
        frame_number = row["frame_number"]
        image_b64 = row["image_b64"]

        if not image_b64:
            continue

        try:
            jpeg_bytes = base64.b64decode(image_b64)
            img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ok, out = cv2.imencode(".jpg", gray)
            if not ok:
                continue

            video_dir = os.path.join(OUTPUT_DIR, video_id)
            os.makedirs(video_dir, exist_ok=True)

            output_path = os.path.join(
                video_dir,
                f"frame_{frame_number:04d}_gray.jpg"
            )

            with open(output_path, "wb") as f:
                f.write(out.tobytes())

        except Exception as e:
            print(f"Error procesando frame {frame_number}: {e}", flush=True)


def save_batch(batch_df, batch_id):
    batch_df.foreachPartition(lambda it: save_partition(it, batch_id))


query = (
    parsed_df.writeStream
    .foreachBatch(save_batch)
    .option("checkpointLocation", CHECKPOINT_DIR)
    .outputMode("append")
    .start()
)

query.awaitTermination()
