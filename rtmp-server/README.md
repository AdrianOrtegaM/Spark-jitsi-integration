````md
# RTMP Server - JitsiToSpark

Servidor RTMP utilizado para la retransmisión multimedia en tiempo real dentro de la arquitectura distribuida desarrollada en el proyecto TFG **JitsiToSpark**.

El sistema permite recibir un flujo RTMP procedente de Jitsi Meet y procesarlo posteriormente mediante Kafka y Spark Streaming.

---

# Arquitectura

El flujo multimedia utilizado sigue la siguiente estructura:

Jitsi Meet → RTMP → MediaMTX → OpenCV/FFmpeg → Kafka → Spark Streaming

---

# Tecnologías utilizadas

- Docker
- MediaMTX
- FFmpeg
- OpenCV
- Python
- Apache Kafka

---

# Estructura del proyecto

```text
rtmp-server/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── frame_extractor.py
├── nginx.conf
│
├── tests/
│   └── prueba_rtmp.py
│
└── README.md
````

---

# Descripción de archivos

| Archivo            | Función                                 |
| ------------------ | --------------------------------------- |
| docker-compose.yml | Despliegue de contenedores              |
| Dockerfile         | Imagen personalizada                    |
| frame_extractor.py | Captura frames RTMP y los envía a Kafka |
| requirements.txt   | Dependencias Python                     |
| nginx.conf         | Configuración del servidor              |
| prueba_rtmp.py     | Script de pruebas RTMP                  |

---

# Requisitos

Es necesario tener instalado:

* Docker
* Docker Compose
* Python 3
* FFmpeg

---

# Puertos utilizados

| Puerto | Servicio |
| ------ | -------- |
| 1935   | RTMP     |
| 9997   | MediaMTX |

---

# Inicio del sistema

Para iniciar el servidor RTMP:

```bash
docker compose up -d
```

Para comprobar los contenedores activos:

```bash
docker ps
```

---

# Flujo RTMP utilizado

La retransmisión multimedia utiliza la siguiente dirección RTMP:

```text
rtmp://IP_SERVIDOR:1935/live/jitsi
```

Esta dirección debe introducirse dentro de Jitsi Meet al iniciar la retransmisión en vivo.

---

# Captura de frames

El procesamiento principal se realiza mediante:

```bash
python frame_extractor.py
```

Este script:

* Accede al stream RTMP.
* Extrae frames mediante FFmpeg.
* Procesa imágenes con OpenCV.
* Envía frames a Apache Kafka.

---

# Script de pruebas

El archivo:

```text
tests/prueba_rtmp.py
```

permite comprobar manualmente la recepción del flujo RTMP y visualizar los frames recibidos en tiempo real.

---

# Problemas encontrados durante el desarrollo

Durante el desarrollo aparecieron diferentes problemas relacionados con:

* Compatibilidad entre versiones de Jitsi.
* Configuración RTMP.
* Permisos Docker.
* Acceso a directorios internos.
* Captura directa desde interfaz web.
* Configuración de puertos.

Finalmente se utilizó:

```text
JITSI_IMAGE_VERSION=stable-9909
```

por proporcionar una mayor estabilidad durante las pruebas realizadas.


