from pyspark.sql import SparkSession
import os

KAFKA_BOOTSTRAP = "kafka:29092"
TOPIC = "raw-frames"

OUTPUT_DIR = "/images/output_clahe"
CHECKPOINT_DIR = "/images/checkpoint_clahe"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

spark = SparkSession.builder.appName("KafkaFramesCLAHE").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "latest")
    .option("failOnDataLoss", "false")
    .load()
)

binary_df = df.select("value")


def save_batch(batch_df, batch_id):
    import cv2
    import numpy as np
    import os

    rows = batch_df.collect()

    if not rows:
        print(f"Batch {batch_id}: sin frames", flush=True)
        return

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    for i, row in enumerate(rows, start=1):
        jpeg_bytes = row["value"]
        if jpeg_bytes is None:
            continue

        img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            continue

        # CLAHE sobre luminancia
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        l_clahe = clahe.apply(l)

        lab_clahe = cv2.merge((l_clahe, a, b))
        processed = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

        output_path = os.path.join(
            OUTPUT_DIR,
            f"batch_{batch_id:04d}_frame_{i:04d}_clahe.jpg"
        )

        cv2.imwrite(output_path, processed)
        print(f"Guardado: {output_path}", flush=True)


query = (
    binary_df.writeStream
    .foreachBatch(save_batch)
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_DIR)
    .start()
)

print(f"Salida en: {OUTPUT_DIR}", flush=True)
query.awaitTermination()
