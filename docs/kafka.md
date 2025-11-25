# Apache Kafka

## 1. Introducción
Apache Kafka es un sistema de mensajería distribuido creado para gestionar datos que fluyen en tiempo real.
Facilita la interacción entre diversas aplicaciones mediante el uso de mensajes agrupados en *temas*.

Kafka es extremadamente escalable, resistente a errores y está ajustado para procesar grandes cantidades de información.

---

## 2. Conceptos fundamentales

### 2.1 Broker
Un **broker** es un servidor Kafka.
Un clúster puede estar formado por uno o varios brokers.

### 2.2 Topic
Un **topic** es un canal donde se publican y consumen mensajes.

Ejemplos:
- `video-events`
- `user-stats`
- `spark-output`

### 2.3 Particiones
Los topics se dividen en **particiones**, que permiten escalar el rendimiento.
Cada partición almacena mensajes de forma ordenada.

### 2.4 Offset
Cada mensaje dentro de una partición tiene un **offset**, que es un identificador único del mensaje.

### 2.5 Producer
Componente que **envía** mensajes a Kafka.
En este proyecto, Spark actuará como *producer*.

### 2.6 Consumer
Componente que **lee** mensajes de Kafka.
En este proyecto, tu microservicio será el *consumer*.

### 2.7 Zookeeper
Kafka depende de Zookeeper para:
- Registrar brokers
- Gestionar particiones
- Mantener el estado del clúster

---

## 3. ¿Para qué se usa Kafka?

- Procesamiento de datos en tiempo real
- Comunicación entre microservicios
- Monitorización y métricas
- Sistemas distribuidos
- Streaming de eventos

En este proyecto, Kafka se utiliza como intermediario entre Spark y otros servicios.

---

## 4. Ejemplo de configuración mínima en Docker Compose

```yaml
version: "3.9"

services:
  zookeeper:
    image: zookeeper:3.7
    ports:
      - "2181:2181"

  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    depends_on:
      - zookeeper
```

---

## 5. Ejemplo: Producer y Consumer

### 5.1 Producer (envío de mensajes)

```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: v.encode('utf-8')
)

producer.send('mi-topic', 'mensaje de prueba')
producer.flush()
```

### 5.2 Consumer (lectura de mensajes)

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'mi-topic',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: v.decode('utf-8')
)

for msg in consumer:
    print(msg.value)
```

---

## 6. Comandos útiles

### 6.1 Crear un topic
```bash
kafka-topics.sh --create --topic mi-topic --bootstrap-server localhost:9092
```

### 6.2 Listar los topics del clúster
```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 6.3 Leer mensajes de un topic
```bash
kafka-console-consumer.sh --topic mi-topic --from-beginning --bootstrap-server localhost:9092
```

### 6.4 Producir mensajes desde consola
```bash
kafka-console-producer.sh --topic mi-topic --bootstrap-server localhost:9092
```

---

## 7. Vinculación con el proyecto

En este trabajo, Apache Kafka funciona como un intermediario entre Spark y el microservicio que transmitirá datos a Jitsi/Jibri.

Kafka posibilita:
- El ingreso de información procesada por Spark en tiempo real
- El transporte de eventos o estadísticas
- La separación de elementos del sistema
- La provisión de tolerancia ante fallos y capacidad de crecimiento

Es un elemento clave para el flujo de datos en el proyecto.

---

## 8. Conclusión

Kafka actúa como un recurso efectivo para transmitir aplicaciones en tiempo real a través de una red de mensajería distribuida.
Su implementación es fundamental en este trabajo para conectar Spark con otros elementos, facilitando un procesamiento confiable, escalable y eficaz.
