from pyspark.sql import SparkSession
import os

KAFKA_BOOTSTRAP = "kafka:29092"
TOPIC = "raw-frames"

BASE_OUTPUT_DIR = "/images/output_kafka_gray"
CHECKPOINT_DIR = "/images/checkpoint_kafka_gray"

os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# carpeta nueva por ejecución: sesion_1, sesion_2, sesion_3...
existing_sessions = []

for item in os.listdir(BASE_OUTPUT_DIR):
    if item.startswith("sesion_"):
        try:
            number = int(item.replace("sesion_", ""))
            existing_sessions.append(number)
        except ValueError:
            pass

next_session = 1 if not existing_sessions else max(existing_sessions) + 1

OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, f"sesion_{next_session}")
os.makedirs(OUTPUT_DIR, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("KafkaFramesToGray")
    .getOrCreate()
)

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
    import os
    import cv2
    import numpy as np

    rows = batch_df.collect()

    if not rows:
        print(f"Batch {batch_id}: sin frames", flush=True)
        return

    print(f"Batch {batch_id}: {len(rows)} frames recibidos", flush=True)

    for i, row in enumerate(rows, start=1):
        jpeg_bytes = row["value"]
        if jpeg_bytes is None:
            continue

        try:
            img = cv2.imdecode(
                np.frombuffer(jpeg_bytes, np.uint8),
                cv2.IMREAD_COLOR
            )

            if img is None:
                print(f"Batch {batch_id}, frame {i}: imagen no válida", flush=True)
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            output_path = os.path.join(
                OUTPUT_DIR,
                f"batch_{batch_id:04d}_frame_{i:04d}_gray.jpg"
            )

            ok = cv2.imwrite(output_path, gray)
            if ok:
                print(f"Guardado: {output_path}", flush=True)
            else:
                print(f"Error guardando: {output_path}", flush=True)

        except Exception as e:
            print(f"Error procesando frame {i} del batch {batch_id}: {e}", flush=True)


query = (
    binary_df.writeStream
    .foreachBatch(save_batch)
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_DIR)
    .start()
)

print(f"Salida en: {OUTPUT_DIR}", flush=True)

query.awaitTermination()
