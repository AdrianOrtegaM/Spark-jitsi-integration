import subprocess
import numpy as np
import cv2
import sys

WIDTH = 1280
HEIGHT = 720
URL = "rtmp://localhost:1935/live/jitsi"

command = [
    "ffmpeg",
    "-loglevel", "warning",
    "-fflags", "nobuffer",
    "-flags", "low_delay",
    "-analyzeduration", "1000000",
    "-probesize", "1000000",
    "-i", URL,
    "-vf", f"scale={WIDTH}:{HEIGHT}",
    "-pix_fmt", "bgr24",
    "-vcodec", "rawvideo",
    "-an",
    "-sn",
    "-f", "rawvideo",
    "-"
]

print("Lanzando FFmpeg lector...")
print(" ".join(command))

pipe = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=10**8
)

frame_size = WIDTH * HEIGHT * 3
contador = 0

while True:
    raw_frame = pipe.stdout.read(frame_size)

    if len(raw_frame) == 0:
        err = pipe.stderr.readline().decode(errors="ignore").strip()
        if err:
            print("FFmpeg:", err)
        else:
            print("Esperando datos del stream...")
        continue

    if len(raw_frame) != frame_size:
        print(f"Frame incompleto: {len(raw_frame)} bytes")
        continue

    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
    contador += 1
    print(f"Frame recibido: {contador}")

    cv2.imshow("RTMP por pipe", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

pipe.terminate()
cv2.destroyAllWindows()
