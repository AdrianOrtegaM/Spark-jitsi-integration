# Jibri

Documentación técnica del componente Jibri utilizado en Jitsi Meet.\
Jibri es el servicio encargado de la grabación y la retransmisión en
vivo (streaming RTMP) de las conferencias.

------------------------------------------------------------------------

## 1. Qué es Jibri

Jibri (Jitsi Broadcasting Infrastructure) es un servicio que
proporciona: - Grabación de reuniones. - Transmisión en vivo mediante
RTMP. - Captura de audio y vídeo a través de una instancia de Google
Chrome controlada.

Jibri actúa como un "cliente oculto" que entra en la sala, captura el
contenido y lo procesa.

------------------------------------------------------------------------

## 2. Arquitectura

Jibri interactúa con los siguientes componentes: - Prosody:
autenticación mediante XMPP. - Jicofo: asignación y gestión de
instancias Jibri. - Jitsi Meet: interfaz desde donde se inicia la
grabación o el streaming.

Flujo simplificado: 1. El usuario solicita grabar/transmitir. 2. Jicofo
selecciona una instancia de Jibri. 3. Jibri entra a la sala como usuario
silencioso. 4. Captura vídeo/audio y lo guarda o envía vía RTMP.

------------------------------------------------------------------------

## 3. Requisitos del sistema

**Hardware recomendado:** - 4 CPU - 4 GB RAM - 20 GB de almacenamiento

**Software necesario:** - Debian o Ubuntu - Google Chrome - FFmpeg -
Xorg - ALSA/Pulseaudio - OpenJDK - Paquete jibri

------------------------------------------------------------------------

## 4. Instalación de Jibri

### 4.1 Actualizar sistema

``` bash
sudo apt update && sudo apt upgrade -y
```

### 4.2 Instalar dependencias

``` bash
sudo apt install default-jre ffmpeg curl unzip xserver-xorg-video-dummy screen alsa-utils xvfb -y
```

### 4.3 Instalar Google Chrome

``` bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

### 4.4 Añadir repositorio oficial e instalar Jibri

``` bash
wget -qO - https://download.jitsi.org/jitsi-key.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/jitsi.gpg
echo "deb [signed-by=/usr/share/keyrings/jitsi.gpg] https://download.jitsi.org stable/" | sudo tee /etc/apt/sources.list.d/jitsi-stable.list
sudo apt update
sudo apt install jibri -y
```

------------------------------------------------------------------------

## 5. Configuración de usuario y permisos

Crear usuario dedicado:

``` bash
sudo adduser jibri
sudo usermod -aG adm,audio,video,plugdev jibri
```

Verificar que pertenece a los grupos: - audio - video

------------------------------------------------------------------------

## 6. Configuración de Jibri

Archivo principal:

``` bash
sudo nano /etc/jitsi/jibri/jibri.conf
```

Configurar: - Dominio XMPP - Usuario de control - Sala de control
(JibriBrewery) - Contraseña del usuario Jibri

Ejemplo:

    xmpp-environment {
      xmpp-server-hosts: ["tu-dominio"]
      xmpp-domain: "tu-dominio"
    }

    control-login {
      domain: "auth.tu-dominio"
      username: "jibri"
      password: "contraseña"
    }

    control-muc {
      domain: "internal.auth.tu-dominio"
      room-name: "JibriBrewery"
      nickname: "jibri-1"
    }

------------------------------------------------------------------------

## 7. Configuración en Prosody

Registrar usuario:

``` bash
sudo prosodyctl register jibri auth.tu-dominio contraseña
```

Habilitar componente para Jibri: Editar:

``` bash
sudo nano /etc/prosody/conf.avail/tu-dominio.cfg.lua
```

Añadir:

    Component "internal.auth.tu-dominio" "muc"
        storage = "memory"
        modules_enabled = { "ping" }

------------------------------------------------------------------------

## 8. Iniciar servicios

``` bash
sudo systemctl restart jibri
sudo systemctl restart prosody
sudo systemctl restart jicofo
```

Ver estado:

``` bash
sudo systemctl status jibri
```

------------------------------------------------------------------------

## 9. Logs

``` bash
sudo journalctl -u jibri -f
sudo tail -f /var/log/jitsi/jibri/log.0.txt
```

------------------------------------------------------------------------

## 10. Pruebas funcionales

En Jitsi Meet: 1. Iniciar una sala. 2. Abrir menú. 3. Seleccionar
"Iniciar grabación".

Correcto si: - Aparece "Grabación iniciada". - Jibri aparece como
usuario oculto.

Para streaming RTMP: - Seleccionar "Transmitir en vivo". - Introducir
URL RTMP.

------------------------------------------------------------------------

## 11. Problemas comunes

### "No Jibri instances available"

-   Jibri no está conectado a XMPP.
-   Revisar credenciales y configuración.

### Errores de audio

-   Revisar grupos audio/video.

### Chrome no inicia

-   Reinstalar Chrome.

### Fallo al iniciar grabación

-   Revisar logs.
-   Verificar puertos abiertos.

------------------------------------------------------------------------

## 12. Conclusión

Jibri es fundamental para la grabación y la retransmisión en Jitsi.\
Esta guía cubre instalación, configuración, puesta en marcha y
diagnóstico de problemas.

