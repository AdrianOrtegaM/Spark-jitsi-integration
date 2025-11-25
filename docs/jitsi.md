# Jitsi Meet

## 1. Introducción
Jitsi Meet es un sistema de videoconferencia de código abierto que utiliza WebRTC. 
Facilita la realización de conferencias de audio y video directamente en el navegador sin requerir la instalación de programas extra.
Su diseño modular posibilita su integración sencilla en diversos entornos.

---

## 2. Arquitectura general

Jitsi Meet está compuesto por varios componentes:

### 2.1 Prosody
- Servidor XMPP utilizado para la señalización.
- Gestiona la comunicación entre los clientes y los servicios internos.

### 2.2 Jicofo
- Coordina las conferencias.
- Gestiona la creación de salas y la negociación WebRTC.
- Interactúa con Jitsi Videobridge.

### 2.3 Jitsi Videobridge (JVB)
- Encargado de reenviar los flujos de vídeo y audio.
- Utiliza un modelo SFU (Selective Forwarding Unit) para optimizar el ancho de banda.

### 2.4 Interfaz Web
- Cliente web que permite unirse a las reuniones.
- Generalmente servido mediante un servidor Nginx.

### 2.5 Jibri (opcional)
- Permite grabación o transmisión en directo de reuniones.
- Se une como un participante más para capturar el contenido.

---

## 3. Características principales

- Basado en WebRTC.
- No necesita instalación del lado del cliente.
- Escalable mediante múltiples instancias de Videobridge.
- Código abierto y gratuito.
- Instalación sencilla mediante Docker.

---

## 4. Integración mediante Docker

El proyecto oficial `docker-jitsi-meet` permite desplegar todos los servicios con Docker Compose, incluyendo:

- Prosody  
- Jicofo  
- Jitsi Videobridge  
- Interfaz Web  
- Jibri (opcional)

Esto facilita el despliegue rápido y la reproducibilidad del entorno.

---

## 5. API externa (uso básico)

Jitsi Meet permite incrustar reuniones en aplicaciones web mediante `external_api.js`.

Ejemplo mínimo:

```html
<script src="https://meet.jit.si/external_api.js"></script>
<div id="meet"></div>

<script>
const api = new JitsiMeetExternalAPI("meet.jit.si", {
    roomName: "MiSala",
    parentNode: document.querySelector('#meet')
});
</script>
```

---

## 6. Casos de uso

- Reuniones online en navegadores web.
- Integración con aplicaciones web.
- Sistemas personalizados de videoconferencia.
- Grabación o streaming mediante Jibri.
- Despliegues con Docker en infraestructuras propias.

---

## 7. Conclusión

Jitsi Meet es una plataforma robusta, versátil y sencilla de instalar de videoconferencia.
Su diseño modular y compatibilidad con contenedores Docker lo hacen perfecto para iniciativas que requieren comunicación inmediata.

