````md id="v8gk31"
# Spark Streaming - JitsiToSpark

Módulo de procesamiento distribuido en tiempo real desarrollado para el proyecto TFG **JitsiToSpark**.

Este sistema consume frames multimedia desde Apache Kafka y aplica diferentes transformaciones de procesamiento de imagen utilizando Apache Spark Streaming y OpenCV.

---

# Arquitectura

El flujo multimedia utilizado sigue la siguiente estructura:

Jitsi Meet → RTMP → MediaMTX → Kafka → Spark Streaming → OpenCV

---

# Tecnologías utilizadas

- Apache Spark Streaming
- Apache Kafka
- OpenCV
- Python
- Docker

---

# Estructura del proyecto

```text
spark/
│
├── docker-compose.yml
├── Dockerfile
│
├── spark_kafka_frames.py
├── spark_frames_to_gray.py
├── spark_kafka_brillo_contraste.py
├── spark_kafka_histograma.py
├── spark_kafka_clahe.py
│
├── tests/
│   └── read_kafka_frames.py
│
├── images/
│   └── .gitkeep
│
├── requirements.txt
├── .gitignore
└── README.md
````

---

# Descripción de scripts

| Script                          | Función                                   |
| ------------------------------- | ----------------------------------------- |
| spark_kafka_frames.py           | Procesamiento principal de frames         |
| spark_frames_to_gray.py         | Conversión de imágenes a escala de grises |
| spark_kafka_brillo_contraste.py | Ajuste de brillo y contraste              |
| spark_kafka_histograma.py       | Ecualización y normalización              |
| spark_kafka_clahe.py            | Mejora de contraste mediante CLAHE        |
| read_kafka_frames.py            | Lectura de mensajes Kafka para pruebas    |

---

# Requisitos

Es necesario tener instalado:

* Docker
* Docker Compose
* Python 3
* Apache Spark
* Apache Kafka

---

# Inicio del sistema

Para iniciar Spark Streaming:

```bash
docker compose up -d
```

Para comprobar los contenedores activos:

```bash
docker ps
```

---

# Kafka

El sistema consume frames desde el tópico:

```text
raw-frames
```

y utiliza el broker:

```text
kafka:29092
```

---

# Procesamiento de imágenes

El sistema permite aplicar diferentes transformaciones multimedia en tiempo real:

* Escala de grises
* Brillo y contraste
* Ecualización de histograma
* CLAHE

Las imágenes procesadas se almacenan automáticamente dentro de la carpeta:

```text
/images/
```

---

# Sesiones automáticas

El sistema genera automáticamente carpetas independientes para cada ejecución:

```text
sesion_1
sesion_2
sesion_3
```

permitiendo separar los resultados obtenidos durante diferentes pruebas.

---

# Checkpoints

Spark Streaming utiliza carpetas de checkpoint para:

* Control de batches
* Recuperación de estado
* Gestión de offsets Kafka

Estas carpetas se generan automáticamente durante la ejecución.

---

# Ejecución manual

Ejemplo de ejecución:

```bash
python spark_kafka_frames.py
```

o:

```bash
spark-submit spark_kafka_frames.py
```

---

# Problemas encontrados durante el desarrollo

Durante el desarrollo aparecieron diferentes problemas relacionados con:

* Configuración de Kafka
* Permisos Docker
* Compatibilidad entre versiones
* Procesamiento distribuido
* Gestión de directorios
* Streaming multimedia en tiempo real

La solución aplicada consistió en ajustar la configuración de Spark, Kafka y Docker hasta conseguir una arquitectura estable para el procesamiento multimedia distribuido.

---

# Carpetas no incluidas en GitHub

Las siguientes carpetas se generan automáticamente y no se incluyen en el repositorio:

```text
images/
output_*/
checkpoint_*/
ivy/
.venv/
```

---

