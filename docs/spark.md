# Apache Spark

## 1. Introducción
Aache Spark es una herramienta de gestión de datos en paralelo creada para manejar grandes cantidades de información.
Facilita el análisis de datos tanto de manera por lotes como en tiempo real, ofreciendo rapidez, resistencia a errores y la capacidad de escalar.

Spark se emplea frecuentemente en iniciativas que requieren el procesamiento constante de datos, como en este trabajo de fin de grado, donde actúa como generador de datos hacia Kafka.

---

## 2. ¿Por qué Spark?
Spark se utiliza porque ofrece:

- Alta velocidad en el procesamiento de datos  
- Procesamiento distribuido  
- APIs sencillas (Python, Java, Scala)  
- Integración directa con Kafka  
- Capacidad de procesar datos en streaming en tiempo real  
- Tolerancia a fallos  

En este proyecto Spark será fundamental para recibir datos, procesarlos y enviarlos a Kafka.

---

## 3. Componentes principales

### 3.1 Driver
El programa principal que coordina la ejecución del trabajo.

### 3.2 Executors
Procesos que ejecutan tareas y devuelven resultados al driver.

### 3.3 Cluster Manager
Gestor de recursos del clúster.  
Puede ser:
- Standalone
- YARN
- Kubernetes

### 3.4 RDD (Resilient Distributed Dataset)
Estructura de datos distribuida. Permite tolerancia a fallos.

### 3.5 DataFrames y Spark SQL
API tabular que permite consultas estructuradas.

### 3.6 Structured Streaming
Sistema de streaming de Spark para procesar datos en tiempo real.  
Este es el sistema que se usará en este proyecto.

---

## 4. Arquitectura de Spark

Spark sigue una arquitectura maestro-trabajador:

- Un **Driver** lanza el programa.
- Varios **Workers** ejecutan tareas.
- Un **Cluster Manager** asigna recursos.

El procesamiento se divide en:
- Jobs
- Stages
- Tasks

---

## 5. Spark Streaming

### ¿Qué es?
Un sistema que permite procesar datos en tiempo real.

Spark consume datos de fuentes como:
- Kafka  
- Sockets  
- Archivos  
- APIs  

Y genera:
- Resultados procesados  
- Datos limpios  
- Estadísticas  

Esto es lo que permite que Spark envíe datos útiles a Kafka para que Jitsi/Jibri los use en el proyecto.

---

## 6. Ejemplo básico: Spark leyendo de Kafka

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder     .appName("SparkKafkaExample")     .getOrCreate()

df = spark   .readStream   .format("kafka")   .option("kafka.bootstrap.servers", "kafka:9092")   .option("subscribe", "mi-topic")   .load()

df2 = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

query = df2.writeStream     .format("console")     .start()

query.awaitTermination()
```

### Explicación
- Se crea una sesión de Spark  
- Se conecta a Kafka  
- Se transforma la clave y el valor a texto  
- Se imprime el streaming por consola  

---

## 7. Spark enviando datos a Kafka

```python
df.writeStream   .format("kafka")   .option("kafka.bootstrap.servers", "kafka:9092")   .option("topic", "spark-output")   .start()
```

Este sistema permitirá enviar a Kafka cualquier información que Spark procese.

---

## 8. Docker Compose: Spark + Kafka (ejemplo mínimo)

```yaml
spark:
  image: bitnami/spark
  environment:
    - SPARK_MODE=master
  ports:
    - "7077:7077"
    - "8080:8080"
```

Este servicio debe conectarse con Kafka, que ya estará definido en tu docker-compose.

---

## 9. Relación con el proyecto TFG

Spark es una pieza clave porque:

- Procesa los datos recibidos en tiempo real  
- Limpia, transforma o genera información necesaria  
- Se conecta a Kafka para enviar datos  
- Permite automatizar análisis o métricas  
- Facilita el flujo Spark → Kafka → Microservicio → Jitsi/Jibri  

Sin Spark, el sistema no podría procesar datos a alta velocidad.

---

## 10. Conclusión

Apache Spark es un sistema de procesamiento distribuido que facilita el manejo de datos tanto en lotes como en tiempo real.   
Su habilidad para conectarse con Kafka lo hace una herramienta fundamental para este proyecto.

