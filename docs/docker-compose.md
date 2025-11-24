# Docker Compose

## ¿Qué es Docker Compose?

Docker Compose es unaherramienta que facilita la definición y ejecución de varios contenedores Docker como un único servicio.
Se utiliza para aplicaciones que necesitan diferentes servicios (por ejemplo, Kafka junto con Zookeeper y Spark).

## ¿Para qué sirve?

- Orquestar varios contenedores fácilmente.  
- Levantar toda tu aplicación con un solo comando: `docker compose up`.  
- Evitar levantar contenedores uno por uno manualmente.  
- Facilitar el desarrollo y la reproducción de entornos.

## ¿Cómo funciona?

Docker Compose utiliza un archivo llamado **docker-compose.yml** donde se describen:
- Servicios (contenedores)
- Imágenes a usar
- Configuración de puertos
- Volúmenes
- Dependencias entre contenedores

## Estructura básica de un docker-compose.yml

```yaml
version: "3.9"

services:
  servicio1:
    image: nombre_imagen
    ports:
      - "puerto_local:puerto_contenedor"

  servicio2:
    image: otra_imagen
    depends_on:
      - servicio1
```

## Ejemplo explicado (Kafka + Zookeeper)

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
    depends_on:
      - zookeeper
```

### Explicación:

- **zookeeper**  
  - Usa la imagen oficial `zookeeper:3.7`  
  - Expone el puerto 2181

- **kafka**  
  - Usa la imagen `wurstmeister/kafka`  
  - Expone el puerto 9092  
  - Necesita que Zookeeper esté levantado primero → `depends_on`

## Comandos útiles

```bash
docker compose up -d
docker compose down
docker compose ps
docker compose logs kafka
```

## Conclusión

Docker Compose es esencial para tu TFG porque necesitas levantar varios servicios a la vez:  
**Kafka, Zookeeper, Spark, Jitsi, Jibri…**  
Con Compose los defines una sola vez y los ejecutas con un único comando.
