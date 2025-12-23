# Apache Kafka – Extracción de datos

## 1. Introducción
Apache Kafka es una plataforma de mensajería distribuida orientada a eventos.
En este Trabajo Fin de Grado se utiliza Kafka como un sistema de extracción y transmisión de datos, permitiendo recoger eventos generados por distintos servicios y consumirlos posteriormente de forma desacoplada.

El objetivo principal es demostrar el uso de Kafka como intermediario entre productores y consumidores, aplicando una arquitectura orientada a eventos en un entorno Dockerizado.

---

## 2. Justificación del uso de Kafka
Kafka se ha seleccionado frente a otras soluciones de mensajería como RabbitMQ o ActiveMQ debido a:
- Alta escalabilidad.
- Persistencia de mensajes.
- Desacoplamiento entre productores y consumidores.
- Uso extendido en entornos profesionales.

Estas características lo convierten en una solución adecuada para la extracción de datos en sistemas distribuidos.

---

## 3. Despliegue con Docker

### 3.1 Estructura del proyecto
```
kafka-docker/
├── docker-compose.yml
└── README.md
```

El archivo `docker-compose.yml` contiene la definición de los servicios necesarios y se documenta de forma independiente.

---

## 4. Puesta en marcha

### Arranque de los servicios
```
docker compose up -d
```

### Comprobación del estado
```
docker compose ps
```

---

## 5. Pruebas de funcionamiento

### 5.1 Creación de un topic
```
docker exec -it kafka kafka-topics \
  --create \
  --topic datos \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

### 5.2 Envío de datos (productor)
```
docker exec -it kafka kafka-console-producer \
  --topic datos \
  --bootstrap-server localhost:9092
```

Ejemplo de mensajes enviados:
```
evento_login usuario1
evento_error servicioX
evento_acceso usuario2
```

### 5.3 Extracción de datos (consumidor)
```
docker exec -it kafka kafka-console-consumer \
  --topic datos \
  --from-beginning \
  --bootstrap-server localhost:9092
```

---

## 6. Resultados obtenidos
- Kafka y Zookeeper se despliegan correctamente mediante Docker.
- Los mensajes enviados por los productores se almacenan correctamente.
- Los consumidores pueden extraer los datos sin pérdida de información.
- El sistema permite una comunicación desacoplada entre servicios.

---

## 7. Integración con otros sistemas
Kafka puede integrarse con otros servicios del proyecto, como Jitsi, mediante la captura de logs y eventos generados por sus contenedores Docker, permitiendo centralizar la extracción de datos.

---

## 8. Trabajo futuro
- Automatizar el arranque mediante scripts bash.
- Integrar Kafka con los logs reales de Jitsi.
- Añadir herramientas de análisis y visualización de eventos.

---

## 9. Conclusión
Apache Kafka ha demostrado ser una solución adecuada para la extracción y transmisión de datos en un entorno distribuido.
