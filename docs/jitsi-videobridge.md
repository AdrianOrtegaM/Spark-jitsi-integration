
# Jitsi Videobridge (JVB)

Documentación técnica del elemento Jitsi Videobridge que se emplea en la
plataforma Jitsi Meet.\
Esta parte se encarga de dirigir y gestionar el tráfico de audio y
video entre los asistentes a una conferencia.


------------------------------------------------------------------------

## 1. Qué es Jitsi Videobridge

Documentación técnica del elemento Jitsi Videobridge que se emplea en la
 plataforma Jitsi Meet.\
 Esta parte se encarga de dirigir y gestionar el tráfico de audio y
 video entre los asistentes a una conferencia.

### Funciones principales:

-   Procesa conexiones WebRTC.\
-   Gestiona el envío y recepción de streams.\
-   Optimiza el consumo de CPU.\
-   Actúa como puente entre Jitsi Meet y los clientes.\
-   Se comunica directamente con Prosody y Jicofo.

------------------------------------------------------------------------

## 2. Arquitectura dentro de Jitsi

El Videobridge trabaja con:

-   Prosody: autenticación y señalización mediante XMPP.
-   Jicofo: controlador y coordinador del Videobridge.
-   Jitsi Meet: interfaz web de la conferencia.
-   WebRTC: canal multimedia entre usuarios y el puente.

Representación simplificada:

Cliente → WebRTC → JVB → WebRTC → Cliente

------------------------------------------------------------------------

## 3. Instalación de Jitsi Videobridge (Debian/Ubuntu)

Instalación independiente, pensada para un servidor dedicado de JVB.

### 3.1 Actualizar sistema

``` bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Instalar Java (requisito de JVB)

``` bash
sudo apt install openjdk-11-jre-headless -y
```

### 3.3 Añadir repositorio oficial de Jitsi

``` bash
wget -qO - https://download.jitsi.org/jitsi-key.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/jitsi.gpg
sudo sh -c "echo 'deb [signed-by=/usr/share/keyrings/jitsi.gpg] https://download.jitsi.org stable/' > /etc/apt/sources.list.d/jitsi-stable.list"
```

### 3.4 Instalar JVB

``` bash
sudo apt update
sudo apt install jitsi-videobridge2 -y
```

------------------------------------------------------------------------

## 4. Configuración básica

### 4.1 Configurar la IP pública

Editar el archivo:

``` bash
sudo nano /etc/jitsi/videobridge/sip-communicator.properties
```

Añadir:

    org.ice4j.ice.harvest.NAT_HARVESTER_LOCAL_ADDRESS=IP_PRIVADA
    org.ice4j.ice.harvest.NAT_HARVESTER_PUBLIC_ADDRESS=IP_PUBLICA

### 4.2 Reiniciar servicio

``` bash
sudo systemctl restart jitsi-videobridge2
sudo systemctl status jitsi-videobridge2
```

------------------------------------------------------------------------

## 5. Comunicación con Jicofo

JVB utiliza un token o clave secreta para conectarse al controlador
Jicofo.

Editar:

``` bash
sudo nano /etc/jitsi/videobridge/config
```

Buscar la línea:

    JVB_SECRET=xxxxxxxxx

Debe coincidir con el valor dentro de:

    /etc/jitsi/jicofo/config

------------------------------------------------------------------------

## 6. Ver logs de JVB

### Logs de ejecución

``` bash
sudo journalctl -u jitsi-videobridge2 -f
```

### Archivo de logs

``` bash
sudo tail -f /var/log/jitsi/jvb.log
```

------------------------------------------------------------------------

## 7. Pruebas funcionales

### 7.1 Ver si está escuchando WebRTC

``` bash
sudo ss -ltnp | grep 10000
```

El puerto UDP 10000 debe estar abierto.

### 7.2 Prueba de conexión desde otro equipo

``` bash
nc -u TU_IP_PUBLICA 10000
```

### 7.3 Verificar conexión con Jicofo

Debe aparecer en el log:

    INFO: Connected to XMPP domain

------------------------------------------------------------------------

## 8. Firewall recomendado

``` bash
sudo ufw allow 10000/udp
sudo ufw allow 5222/tcp
sudo ufw allow 5347/tcp
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp
```

------------------------------------------------------------------------

## 9. Escalado horizontal

Se pueden desplegar varios JVBs y conectarlos al mismo servidor
principal.

Ventajas: - Distribución de carga.\
- Menos saturación por servidor.\
- Mayor estabilidad.

Requisitos: - Copiar la misma configuración XMPP.\
- Conectar cada JVB al mismo Prosody.\
- Ajustar tokens de conexión.

------------------------------------------------------------------------

## 10. Conclusión

Jitsi Videobridge es el componente central encargado de la transmisión
multimedia en Jitsi.\
Con esta guía se puede instalar, configurar y realizar pruebas básicas.\
Forma parte esencial del TFG, especialmente para evaluar el rendimiento
y estabilidad del sistema.
