# RFC 5374

Documentación teórica sobre el RFC 5374 y el modelo de comunicación
multicast aplicado a sistemas distribuidos.  
Este documento sirve como base conceptual para comprender arquitecturas
uno-a-muchos utilizadas en el proyecto.

------------------------------------------------------------------------

## 1. Qué es el RFC 5374

El RFC 5374 es un documento técnico que define el **modelo de asignación
de direcciones IP multicast**. Su objetivo principal es estandarizar la
forma en la que se organizan y utilizan las direcciones multicast para
permitir la comunicación entre un emisor y múltiples receptores.

Este estándar forma parte de la base teórica de las **arquitecturas
uno-a-muchos**, ampliamente utilizadas en redes y sistemas distribuidos.

------------------------------------------------------------------------

## 2. Qué es la comunicación multicast

La comunicación multicast es un modelo de transmisión en el que un único
emisor envía información a un grupo de receptores simultáneamente.

A diferencia de otros modelos:
- Unicast: comunicación uno-a-uno.
- Broadcast: comunicación uno-a-todos.
- Multicast: comunicación uno-a-muchos.

Los receptores solo reciben los mensajes si pertenecen al grupo
multicast correspondiente.

------------------------------------------------------------------------

## 3. Multicast y su pila de red

La comunicación multicast se apoya en el protocolo **IP (Internet
Protocol)** y está disponible tanto en **IPv4** como en **IPv6**.

### Multicast en IPv4
- Direcciones de **32 bits**
- Rango reservado: 224.0.0.0 – 239.255.255.255
- Utiliza grupos multicast para la distribución de datos.

### Multicast en IPv6
- Direcciones de **128 bits**
- Prefijo multicast:FF00::/8
- Mejora la escalabilidad y la organización de grupos frente a IPv4.

------------------------------------------------------------------------

## 4. Asignación de direcciones multicast

El RFC 5374 define cómo deben asignarse las direcciones multicast para:
- Evitar conflictos entre aplicaciones.
- Permitir una gestión ordenada de los grupos.
- Facilitar la escalabilidad en redes grandes.

La asignación correcta es fundamental para garantizar un funcionamiento
eficiente de la comunicación multicast.

------------------------------------------------------------------------

## 5. Para qué sirve el multicast

El multicast se utiliza en escenarios donde:
- Un mismo mensaje debe llegar a múltiples receptores.
- Se quiere optimizar el uso del ancho de banda.
- Se requiere escalabilidad.
- Los emisores y receptores deben estar desacoplados.

Casos de uso habituales:
- Streaming de vídeo o audio.
- Sistemas de monitorización.
- Distribución de eventos.
- Sistemas distribuidos.

------------------------------------------------------------------------

## 6. Relación con este proyecto

Este proyecto no implementa multicast IP de forma directa, pero sí
aplica el **modelo conceptual definido en el RFC 5374**.

En lugar de direcciones multicast, se utilizan mecanismos de alto nivel
como:
- Productores de eventos.
- Canales o topics de distribución.
- Consumidores suscritos a dichos eventos.

Este enfoque permite que múltiples consumidores reciban la misma
información sin que el productor tenga conocimiento directo de ellos,
siguiendo el principio uno-a-muchos.

------------------------------------------------------------------------

## 7. Importancia del RFC 5374 en el TFG

El RFC 5374 aporta:
- Base teórica sobre comunicación uno-a-muchos.
- Justificación del desacoplamiento entre componentes.
- Fundamento de escalabilidad en sistemas distribuidos.
- Contexto de redes aplicado a arquitecturas orientadas a eventos.


