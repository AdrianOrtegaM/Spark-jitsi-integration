````md id="v3p9yr"
# JitsiToSpark

Arquitectura distribuida para el procesamiento multimedia en tiempo real utilizando Jitsi Meet, RTMP, Apache Kafka y Apache Spark Streaming.

Proyecto desarrollado como Trabajo de Fin de Grado del Grado en Ingeniería Informática de la Universidad de Burgos.

---

# Descripción del proyecto

El sistema desarrollado permite capturar videollamadas realizadas mediante Jitsi Meet y procesarlas en tiempo real utilizando tecnologías distribuidas.

La arquitectura implementada retransmite el flujo multimedia mediante RTMP hacia un servidor intermedio, desde donde los frames son capturados y enviados a Apache Kafka para su posterior procesamiento distribuido mediante Spark Streaming.

El objetivo principal del proyecto es desarrollar una arquitectura modular capaz de procesar información multimedia en tiempo real utilizando sistemas distribuidos.

---

# Arquitectura general

El flujo multimedia implementado sigue la siguiente estructura:


Jitsi Meet
    ↓
RTMP (MediaMTX)
    ↓
OpenCV / FFmpeg
    ↓
Apache Kafka
    ↓
Apache Spark Streaming
    ↓
Procesamiento multimedia
````

---

# Tecnologías utilizadas

* Jitsi Meet
* Docker
* MediaMTX
* RTMP
* FFmpeg
* OpenCV
* Apache Kafka
* Apache Spark Streaming
* Python

---

# Estructura del proyecto

```text
Proyecto-TFG/
│
├── jitsi/
│
├── rtmp-server/
│
├── kafka/
│
├── spark/
│
└── README.md
```

---

# Descripción de módulos

| Módulo      | Función                                   |
| ----------- | ----------------------------------------- |
| jitsi       | Sistema de videollamadas                  |
| rtmp-server | Retransmisión RTMP y extracción de frames |
| kafka       | Sistema distribuido de mensajería         |
| spark       | Procesamiento multimedia distribuido      |

---

# Requisitos

Es necesario disponer de:

* Docker
* Docker Compose
* Python 3
* Apache Spark
* Apache Kafka

---

# Inicio del sistema

## 1. Iniciar Jitsi Meet

```bash
docker compose up -d
```

## 2. Iniciar RTMP Server

```bash
docker compose up -d
```

## 3. Iniciar Kafka

```bash
docker compose up -d
```

## 4. Iniciar Spark Streaming

```bash
docker compose up -d
```

---

# Retransmisión RTMP

La retransmisión multimedia utiliza la dirección:

```text
rtmp://IP_SERVIDOR:1935/live/jitsi
```

Esta dirección debe introducirse en Jitsi Meet al iniciar una transmisión en vivo.

---

# Procesamiento multimedia

El sistema permite aplicar diferentes transformaciones sobre los frames recibidos:

* Escala de grises
* Ajuste de brillo y contraste
* Ecualización de histograma
* CLAHE

---

# Características principales

* Procesamiento multimedia en tiempo real
* Arquitectura distribuida
* Comunicación mediante Kafka
* Streaming RTMP
* Procesamiento paralelo con Spark Streaming
* Captura automática de frames
* Sistema modular y escalable

---

# Problemas encontrados durante el desarrollo

Durante el desarrollo aparecieron diferentes problemas relacionados con:

* Compatibilidad entre versiones de Jitsi
* Configuración RTMP
* Permisos Docker
* Configuración WebRTC
* Gestión de puertos
* Procesamiento distribuido
* Streaming multimedia

Finalmente se utilizó:

```text
JITSI_IMAGE_VERSION=stable-9909
```

por proporcionar una mayor estabilidad durante las pruebas realizadas.

---

# Carpetas no incluidas en GitHub

Algunas carpetas y archivos se generan automáticamente durante la ejecución y no forman parte del repositorio:

```text
recordings/
images/
output_*/
checkpoint_*/
frames_live/
ivy/
.venv/
*.mp4
*.jpg
```
# Licencia

Este proyecto ha sido desarrollado con fines académicos como parte del Trabajo de Fin de Grado del Grado en Ingeniería Informática de la Universidad de Burgos.

El código fuente se proporciona únicamente con fines educativos y de consulta.
---

