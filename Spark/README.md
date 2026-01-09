# Apache Spark – Procesamiento de datos con Docker

## 1. Introducción

Apache Spark es un motor de procesamiento distribuido diseñado para el análisis y transformación de grandes volúmenes de datos de forma eficiente.

En este proyecto se utiliza Apache Spark como sistema de procesamiento de datos, desplegado en modo standalone mediante Docker Compose. El objetivo es ejecutar jobs distribuidos y validar el procesamiento de datos reales dentro de un entorno controlado y reproducible.

---

## 2. Arquitectura del sistema

El sistema se compone de los siguientes elementos:

- **Spark Master**
  - Coordina el clúster
  - Asigna recursos a los workers
  - Proporciona una interfaz web de monitorización

- **Spark Worker**
  - Ejecuta las tareas distribuidas
  - Consume los recursos asignados por el Master

- **Red Docker dedicada**
  - Permite la comunicación interna entre los servicios

- **Volúmenes compartidos**
  - Permiten persistir los datos de entrada y salida fuera de los contenedores

Esta arquitectura permite escalar el sistema fácilmente añadiendo nuevos workers.

---

## 3. Despliegue con Docker Compose

El despliegue de Apache Spark se realiza mediante Docker Compose, utilizando una arquitectura standalone con un nodo master y un worker.

Los contenedores se ejecutan de forma aislada y se comunican a través de una red bridge definida específicamente para el clúster.

---

## 4. Estructura del proyecto

```
spark/
├── docker-compose.yml
├── images/
│   ├── input/
│   │   └── animal.jpeg
│   └── output/
│       └── animal_gray.jpeg
```

- `images/input/` contiene los datos de entrada
- `images/output/` almacena los resultados generados por Spark

---

## 5. Puesta en marcha

Arranque del clúster:

```
docker compose up -d
```

Comprobación del estado de los contenedores:

```
docker ps
```

Acceso a la interfaz web del Spark Master:

```
http://localhost:9090
```

---

## 6. Validación del funcionamiento

El correcto funcionamiento del clúster se validó mediante:

- Visualización del worker activo en la interfaz web
- Ejecución de aplicaciones distribuidas mediante `spark-submit`
- Monitorización de aplicaciones en estado RUNNING y COMPLETED
- Consumo de recursos por parte del worker durante la ejecución de jobs

Estas pruebas confirman que Spark ejecuta correctamente tareas distribuidas.

---

## 7. Caso de uso implementado

Como prueba funcional se implementó un caso de uso de procesamiento de imágenes:

- Lectura de una imagen en formato JPEG
- Procesamiento de los datos mediante una transformación a escala de grises
- Almacenamiento del resultado como fichero de salida

La validación se realizó de forma visual, comprobando que la imagen generada corresponde al resultado esperado.

---

## 8. Aspectos aprendidos y consideraciones

Durante el desarrollo se tuvieron en cuenta los siguientes aspectos:

- Gestión de puertos para evitar conflictos con otros servicios
- Uso de volúmenes para la persistencia de datos
- Instalación de dependencias adicionales dentro del contenedor
- Diferencias entre ejecutar Spark en modo interactivo y mediante `spark-submit`
- Importancia de la monitorización mediante la interfaz web

Estos puntos reflejan situaciones habituales en entornos reales.

---

## 9. Posibles ampliaciones

El sistema puede ampliarse fácilmente para:

- Añadir más Spark Workers
- Integrar Spark con sistemas de mensajería
- Procesar múltiples datos en paralelo
- Automatizar el despliegue completo
- Crear una imagen Docker personalizada con dependencias incluidas

---

## 10. Conclusión

Apache Spark ha demostrado ser una herramienta eficaz para el procesamiento distribuido de datos dentro de un entorno contenerizado. El despliegue mediante Docker Compose permite validar su funcionamiento de forma sencilla, reproducible y escalable.
