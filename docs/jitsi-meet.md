# Jitsi Meet

## 1. Introducción
Jitsi Meet es una herramienta de videoconferencia de código abierto que utiliza WebRTC. Permite llevar a cabo conferencias de audio y video sin requerir la instalación de programas adicionales y opera totalmente desde el navegador. Su diseño modular permite su implementación en entornos distribuidos a través de contenedores. 

En este trabajo, Jitsi Meet sirve como el destino final para el flujo multimedia que es procesado por Spark y distribuido a través de Kafka. 

---

## 2. Arquitectura de Jitsi Meet

Jitsi Meet está compuesto por varios servicios principales:

### 2.1 Prosody (servidor XMPP)
- Gestiona la señalización.
- Autentica a los clientes.
- Coordina la negociación WebRTC entre usuarios y servicios.

### 2.2 Jicofo (Jitsi Conference Focus)
- Administra la creación y gestión de conferencias.
- Interactúa con el Videobridge.
- Decide qué Videobridge usa cada sala.

### 2.3 Jitsi Videobridge (JVB)
- Componente clave que envía y recibe flujos multimedia.
- Utiliza el modelo SFU (Selective Forwarding Unit) para reenviar vídeo/audio de forma eficiente.
- Maneja los flujos WebRTC de todos los participantes.

### 2.4 Interfaz Web
- La interfaz con la que interactúan los usuarios.
- Se sirve generalmente mediante un servidor Nginx.

### 2.5 Jibri (opcional)
- Permite grabar o retransmitir las reuniones.
- Funciona como un “usuario virtual” que entra a la sala y captura la sesión.

---

## 3. Funcionamiento Interno

El flujo básico de Jitsi Meet es:

1. El usuario accede a la interfaz web.
2. El navegador inicia la señalización mediante Prosody (protocolo XMPP).
3. Jicofo crea o asigna una sala.
4. Jitsi Videobridge gestiona el vídeo/audio entre todos los usuarios.
5. Jibri, si está activado, graba o retransmite la sesión.

---

## 4. Uso en el Proyecto (TFG)

El proyecto sigue esta arquitectura:

**Spark → Kafka → Microservicio → Jitsi/Jibri**

Jitsi Meet se utiliza para:

- Visualización del flujo multimedia generado tras el procesamiento.
- Creación de salas de prueba para mostrar los resultados.
- Posible retransmisión o grabación mediante Jibri.

---

## 5. Despliegue con Docker

El repositorio oficial `docker-jitsi-meet` permite levantar toda la arquitectura mediante Docker Compose, incluyendo:

- Prosody  
- Jicofo  
- Jitsi Videobridge  
- Interfaz Web  
- Jibri (opcional)

El archivo `docker-compose.yml` contiene la definición completa de estos servicios.

---

## 6. Ventajas de usar Jitsi Meet

- Tecnología WebRTC de baja latencia.
- Código abierto y configurable.
- Modular y escalable.
- Muy fácil de desplegar en contenedores.
- Encaja perfectamente con arquitecturas de microservicios.

---

## 7. Conclusión

Jitsi Meet es la parte final del sistema donde se observa el contenido multimedia creado por Spark y enviado a través de Kafka. Su diseño basado en WebRTC y su capacidad para funcionar con Docker lo hacen la opción perfecta para finalizar el proceso del proyecto.
