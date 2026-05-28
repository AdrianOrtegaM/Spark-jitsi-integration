import subprocess
import time
import threading
import cv2
import numpy as np
from kafka import KafkaProducer

RTMP_URL = "rtmp://mediamtx:1935/live"
KAFKA_BROKER = "kafka:29092"
TOPIC = "raw-frames"


def wait_for_kafka():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: v
            )
            print("Conectado a Kafka", flush=True)
            return producer
        except Exception as e:
            print(f"Kafka no disponible todavía: {e}", flush=True)
            time.sleep(5)


def drain_stderr(pipe):
    for line in iter(pipe.stderr.readline, b""):
        msg = line.decode(errors="ignore").strip()
        if msg:
            print(f"FFmpeg stderr: {msg}", flush=True)


def start_ffmpeg():
    command = [
        "ffmpeg",
        "-loglevel", "info",
        "-i", RTMP_URL,
        "-an",
        "-sn",
        "-vf", "fps=1,scale=640:360",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-"
    ]

    print("Lanzando FFmpeg:", " ".join(command), flush=True)

    pipe = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=10**8
    )

    threading.Thread(target=drain_stderr, args=(pipe,), daemon=True).start()
    return pipe


def main():
    producer = wait_for_kafka()

    while True:
        print("Intentando conectar al stream RTMP...", flush=True)
        pipe = start_ffmpeg()
        buffer = b""

        try:
            while True:
                chunk = pipe.stdout.read(4096)
                print(f"Bytes recibidos: {len(chunk) if chunk else 0}", flush=True)

                if not chunk:
                    print("Sin datos del stream, reintentando...", flush=True)
                    break

                buffer += chunk

                while True:
                    start = buffer.find(b"\xff\xd8")
                    end = buffer.find(b"\xff\xd9")

                    if start != -1 and end != -1 and end > start:
                        jpg = buffer[start:end + 2]
                        buffer = buffer[end + 2:]

                        frame = cv2.imdecode(
                            np.frombuffer(jpg, dtype=np.uint8),
                            cv2.IMREAD_COLOR
                        )

                        if frame is None:
                            continue

                        ok, encoded = cv2.imencode(".jpg", frame)
                        if not ok:
                            continue

                        producer.send(TOPIC, encoded.tobytes())
                        print("Frame enviado a Kafka", flush=True)
                    else:
                        break

        except Exception as e:
            print(f"Error leyendo stream: {e}", flush=True)

        finally:
            try:
                pipe.kill()
            except Exception:
                pass
            time.sleep(3)


if __name__ == "__main__":
    main()
