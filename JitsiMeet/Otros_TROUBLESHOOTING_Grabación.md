# Jitsi Meet + Jibri (Docker) -- Guía Completa de Problemas y Soluciones

Este documento recopila TODOS los errores reales encontrados durante el
despliegue de Jitsi Meet con grabación (Jibri) en entorno local Docker,
junto con sus causas técnicas y soluciones aplicadas.

Este README está pensado como referencia para cualquier persona que
tenga problemas similares.

------------------------------------------------------------------------

# 1. Error: Jibri no puede iniciar grabación

## Mensaje típico:

FailedToJoinCall SESSION Failed to join the call

## Causa:

Jibri no puede abrir la URL de la sala mediante Selenium (ChromeDriver).

## Motivo real más común:

Dentro del contenedor Docker, el dominio interno (ej: jitsi.local) no
resuelve correctamente al servicio web en el puerto 443.

## Solución:

En docker-compose.yml, añadir en el servicio jibri:

links: - web:jitsi.local

Esto hace que dentro del contenedor Jibri, https://jitsi.local apunte
correctamente al servicio web interno (puerto 443).

------------------------------------------------------------------------

# 2. Error: net::ERR_CONNECTION_REFUSED

## Causa:

Jibri intenta acceder a https://jitsi.local pero Docker no redirige al
puerto correcto.

## Solución:

NO usar la IP del host para Jibri. Jibri debe usar el dominio interno
(XMPP_DOMAIN) y resolverse dentro de Docker.

Comprobar desde el contenedor: docker exec -it
`<jibri_container>`{=html} bash -lc 'curl -kI https://jitsi.local'

Debe devolver HTTP 200 o 302.

------------------------------------------------------------------------

# 3. Error: cap_sys_admin not permitted

## Causa:

Jibri necesita capacidades elevadas para ejecutar Chrome dentro del
contenedor.

## Solución en docker-compose.yml:

privileged: true cap_add: - SYS_ADMIN - NET_ADMIN

------------------------------------------------------------------------

# 4. Error: DISPLAY variable not set

## Causa:

Jibri usa un entorno gráfico virtual para Chrome.

## Solución:

Añadir en jibri:

DISPLAY=:0

------------------------------------------------------------------------

# 5. Grabación no genera archivo MP4

## Causas posibles:

-   Jibri falla antes de comenzar a grabar
-   Problemas de permisos en carpeta recordings
-   finalize.sh no existe o no es ejecutable

## Solución de permisos:

sudo mkdir -p \~/.jitsi-meet-cfg/jibri/recordings sudo chown -R
1000:1000 \~/.jitsi-meet-cfg/jibri sudo chmod -R 777
\~/.jitsi-meet-cfg/jibri

## finalize.sh mínimo recomendado:

#!/bin/bash set -e exit 0

Dar permisos: chmod +x \~/.jitsi-meet-cfg/jibri/finalize.sh

------------------------------------------------------------------------

# 6. Stop Recording parece no detener

## Síntoma:

La interfaz sigue mostrando "Recording..." hasta que sales de la sala.

## Realidad:

En muchos casos la grabación SÍ se detiene, pero la UI tarda en
actualizar.

## Cómo comprobarlo:

docker compose logs --tail=200 jibri \| grep "BUSY -\> IDLE"

Si aparece BUSY -\> IDLE, está detenido correctamente.

## Mejora recomendada:

Añadir en jibri:

JIBRI_SINGLE_USE_MODE=true

Esto limpia el estado tras cada grabación.

------------------------------------------------------------------------

# 7. Error NoSuchSessionException (Selenium)

## Mensaje típico:

Session ID is null. Using WebDriver after calling quit()?

## Causa:

Condición de carrera en Selenium cuando ChromeDriver ya se cerró.

## Impacto:

Normalmente es ruido y no rompe la grabación si el archivo ya fue
creado.

------------------------------------------------------------------------

# 8. 400 Bad Request (plain HTTP request sent to HTTPS port)

## Causa:

Acceder por http:// en puerto HTTPS.

## Solución:

Usar siempre: https://IP:8443/

------------------------------------------------------------------------

# 9. Jibri no aparece detectado en Jicofo

## Causa:

Faltan variables ENABLE_RECORDING o configuración del brewery MUC.

## Verificación:

docker compose logs jicofo \| grep brewery

Debe mostrar que se unió correctamente.

------------------------------------------------------------------------

# 10. Comandos útiles de diagnóstico

Ver estado Jibri: docker compose logs --tail=200 jibri

Ver detección en Jicofo: docker compose logs --tail=200 jicofo

Ver archivos generados: ls -lah \~/.jitsi-meet-cfg/jibri/recordings

------------------------------------------------------------------------

# Conclusión

Los problemas más comunes suelen deberse a:

-   Resolución incorrecta de dominio dentro de Docker
-   Permisos en carpeta recordings
-   Falta de capacidades SYS_ADMIN
-   Flags incorrectos de Chrome
-   finalize.sh inexistente
-   UI que no refleja estado real

Con la configuración correcta de docker-compose, permisos adecuados y
dominio interno bien resuelto, Jibri funciona correctamente en entorno
LAN con IP pública interna, por eso revisar esta fichero para solucionar los errores de grabación.

