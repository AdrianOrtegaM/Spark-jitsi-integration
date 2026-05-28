from kafka import KafkaConsumer
from pathlib import Path
import time

TOPIC = "raw-frames"
BOOTSTRAP = "localhost:9092"
BASE_DIR = Path("/home/ortis/Documentos/rtmp-server/frames_live")

INTERVAL = 1  # 1 frame por segundo


def get_next_folder(base_dir: Path) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)

    existing_numbers = []
    for item in base_dir.iterdir():
        if item.is_dir() and item.name.startswith("Carpeta_"):
            suffix = item.name.replace("Carpeta_", "")
            if suffix.isdigit():
                existing_numbers.append(int(suffix))

    next_number = 1 if not existing_numbers else max(existing_numbers) + 1
    folder = base_dir / f"Carpeta_{next_number}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def main():
    output_dir = get_next_folder(BASE_DIR)
    print(f"Guardando frames en: {output_dir}")

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        auto_offset_reset="latest",
        enable_auto_commit=False,
    )

    latest_frame = None
    last_save_time = time.time()
    count = 0

    try:
        while True:
            records = consumer.poll(timeout_ms=200)

            # Guardar el último frame recibido
            for partition in records.values():
                for msg in partition:
                    latest_frame = msg.value

            now = time.time()

            # Guardar 1 frame por segundo
            if latest_frame is not None and (now - last_save_time) >= INTERVAL:
                count += 1
                frame_path = output_dir / f"frame_{count:03d}.jpg"

                with open(frame_path, "wb") as f:
                    f.write(latest_frame)

                print(f"Guardado: {frame_path}")

                last_save_time = now

    except KeyboardInterrupt:
        print("\nDetenido por usuario")

    finally:
        consumer.close()

    print(f"Total frames guardados: {count}")


if __name__ == "__main__":
    main()
