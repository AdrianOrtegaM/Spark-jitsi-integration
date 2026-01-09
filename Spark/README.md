Apache Spark – Despliegue con Docker Compose

Este repositorio contiene la configuración y documentación para el despliegue de un
clúster Apache Spark en modo standalone utilizando Docker Compose.
El entorno está orientado a la ejecución de jobs distribuidos y al procesamiento
de datos.


OBJETIVO DEL PROYECTO

El objetivo principal de este proyecto es:

- Desplegar Apache Spark de forma reproducible mediante contenedores
- Validar el funcionamiento de un clúster distribuido (Master + Worker)
- Procesar datos reales y almacenar los resultados
- Comprender los problemas reales de integración, dependencias y persistencia de datos


ARQUITECTURA DEL SISTEMA

El sistema se basa en una arquitectura de:

- Spark Master
  - Gestiona el clúster
  - Asigna tareas a los workers
  - Proporciona una interfaz web de monitorización

- Spark Worker
  - Ejecuta las tareas distribuidas
  - Consume los recursos asignados por el Master

- Red Docker dedicada
  - Permite la comunicación interna entre los servicios

- Volúmenes compartidos
  - Permiten persistir datos de entrada y salida fuera de los contenedores

Esta arquitectura permite escalar el sistema fácilmente añadiendo más workers
en el futuro.


PERSISTENCIA DE DATOS
-Ejemplo de uso-
Se utiliza un volumen compartido para trabajar con datos reales:

- Datos de entrada: imágenes originales
- Datos de salida: imágenes procesadas

Esto permite:
- Mantener los resultados aunque los contenedores se reinicien
- Verificar visualmente que Spark ha procesado correctamente los datos
- Separar claramente infraestructura y datos


VALIDACIÓN DEL FUNCIONAMIENTO

El correcto funcionamiento del clúster se comprobó mediante:

- Acceso a la interfaz web del Spark Master
- Visualización de workers activos
- Ejecución de aplicaciones distribuidas
- Monitorización de aplicaciones en estado RUNNING y COMPLETED
- Procesamiento de datos reales con generación de resultados persistentes

Estas pruebas confirman que Spark no solo está levantado, sino que ejecuta
jobs reales correctamente.


CASO DE USO IMPLEMENTADO

Como prueba funcional se implementó un caso de uso de procesamiento de imágenes,
en el que:

- Se leyó una imagen en formato JPEG como dato de entrada
- Se aplicó una transformación (conversión a escala de grises)
- Se almacenó la imagen resultante como salida

La validación se realizó de forma visual, comprobando que la imagen generada
corresponde al resultado esperado.


ASPECTOS APRENDIDOS Y CONSIDERACIONES IMPORTANTES

Durante el desarrollo se aprendieron y tuvieron en cuenta los siguientes puntos:

- No todos los contenedores necesitan exponer puertos al host
- Los conflictos de puertos son comunes cuando conviven varios servicios
- Las imágenes Docker oficiales suelen ser mínimas y requieren dependencias adicionales
- Algunas librerías externas requieren dependencias nativas del sistema
- Las instalaciones realizadas dentro de un contenedor no son persistentes si se elimina
- Es importante separar claramente:
  - Infraestructura
  - Datos
  - Código

Estos aspectos reflejan problemas reales que aparecen en entornos profesionales.


CONCLUSIÓN

Este despliegue demuestra el uso de Apache Spark como motor de procesamiento
distribuido dentro de un entorno contenerizado, validando tanto su funcionamiento
técnico como su aplicabilidad a casos reales de procesamiento de datos.
