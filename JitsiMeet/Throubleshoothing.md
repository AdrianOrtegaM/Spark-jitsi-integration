## Troubleshooting: despliegue de Jitsi Meet con Docker en entorno local

Este documento describe de forma detallada todos los problemas encontrados durante el despliegue de Jitsi Meet usando Docker en un entorno local, así como las causas técnicas reales de cada fallo y las soluciones aplicadas.
El objetivo es servir como referencia y aprendizaje para futuros despliegues similares.

---

## Contexto inicial

El despliegue se realizó usando `docker-compose` con los siguientes servicios:

- web
- prosody
- jicofo
- jvb
- coturn

El objetivo era disponer de un servidor Jitsi Meet accesible desde PC, móvil y tablet dentro de una red local, permitiendo múltiples usuarios simultáneos.

---

## 1. No se podía entrar a ninguna reunión

### Síntomas
- La web de Jitsi cargaba correctamente.
- Al pulsar “Empezar reunión” no se entraba en la sala.
- La interfaz quedaba en estado “Conectando”.
- En los logs de `jicofo` aparecían errores como:

```text
UnknownHostException: xmpp.meet.jitsi
```

### Causa
Parte del sistema seguía intentando conectarse al dominio por defecto `meet.jitsi`, mientras que el dominio configurado realmente era `jitsi.local`.
Esto provocaba que Jicofo no pudiera resolver el servidor XMPP.

La causa raíz fue una desalineación de dominios XMPP entre el archivo `.env`, el archivo `docker-compose.yml` y la configuración generada por Prosody.

### Solución
Unificar todos los dominios XMPP en el archivo `.env`:

```env
XMPP_DOMAIN=jitsi.local
XMPP_AUTH_DOMAIN=auth.jitsi.local
XMPP_MUC_DOMAIN=muc.jitsi.local
XMPP_INTERNAL_MUC_DOMAIN=internal-muc.jitsi.local
XMPP_GUEST_DOMAIN=guest.jitsi.local
```

Después, eliminar completamente la configuración previa y regenerarla:

```bash
docker compose down
rm -rf ~/.jitsi-meet-cfg
docker compose up -d
```

---

## 2. Jicofo no conseguía conectarse a Prosody

### Síntomas
- Jicofo entraba en un bucle constante de reconexión.
- En los logs aparecían errores como:

```text
Failed to connect/login
Connection refused
```

### Causa
Jicofo no tenía definido explícitamente a qué servidor XMPP debía conectarse.
En entornos Docker, si no se especifica el servidor, la resolución automática puede fallar.

### Solución
Definir explícitamente el servidor y el puerto XMPP en el servicio `jicofo` dentro de `docker-compose.yml`:

```env
XMPP_SERVER=prosody
XMPP_PORT=5222
```

Tras este cambio, Jicofo pudo conectarse correctamente, autenticarse y descubrir los componentes XMPP necesarios.

---

## 3. JVB no se conectaba correctamente o expulsaba a los usuarios

### Síntomas
- La sala se creaba, pero no había audio o vídeo.
- Los usuarios eran expulsados de la reunión.
- En los logs de `jvb` aparecían errores como:

```text
UnknownHostException: prosody
```

### Causa
El contenedor JVB utilizaba:

```yaml
network_mode: host
```

En este modo, Docker no proporciona DNS interno, por lo que los nombres de servicio como `prosody` pueden no resolverse correctamente.

### Solución
Mantener `network_mode: host` (necesario para WebRTC), asegurar que Prosody estuviera completamente levantado antes de JVB y reiniciar el stack tras limpiar la configuración.

La solución se confirmó cuando JVB apareció correctamente registrado en:

```text
jvbbrewery@internal-muc.jitsi.local
```

---

## 4. Problemas de permisos en el directorio de configuración

### Síntomas
- No se podían borrar archivos dentro de `~/.jitsi-meet-cfg`.
- Aparecían errores de “Permiso denegado”.
- Los cambios de configuración no se aplicaban.

### Causa
Los contenedores de Jitsi crean archivos como usuario `root`, lo que provoca conflictos con el usuario local del sistema.

### Solución
Corregir la propiedad y los permisos del directorio:

```bash
sudo chown -R usuario:usuario ~/.jitsi-meet-cfg
sudo chmod -R u+rwX,go+rX ~/.jitsi-meet-cfg
```

Después, reiniciar los contenedores.

---

## 5. Solo podía entrar un usuario a la vez

### Síntomas
- Al entrar desde el móvil, el usuario del PC era expulsado.
- Al volver a entrar desde el PC, el móvil se desconectaba.

### Causa real
No era un problema de autenticación.
El problema estaba relacionado con WebRTC e ICE: el servidor anunciaba el dominio `jitsi.local`, que no era resoluble por los dispositivos móviles, provocando fallos de renegociación.

### Solución
Usar una URL accesible por todos los dispositivos de la red local configurando `PUBLIC_URL` con la IP del servidor:

```env
PUBLIC_URL=https://192.168.1.131:8443
```

Además, permitir invitados:

```env
ENABLE_AUTH=0
ENABLE_GUESTS=1
```

---

## 6. Estado final del sistema

Tras aplicar todas las correcciones:
- Todos los contenedores estaban en estado `Up`.
- Jicofo conectado correctamente a Prosody.
- JVB registrado en el brewery.
- Acceso funcional desde PC, móvil y tablet.
- Múltiples usuarios simultáneos sin desconexiones.

---

## Conclusión

Los principales problemas encontrados se debieron a dominios XMPP mal alineados, supuestos incorrectos sobre DNS en Docker, uso de `network_mode: host` sin considerar sus implicaciones, problemas de permisos en volúmenes persistentes y uso de dominios locales no resolubles por dispositivos móviles.

Una configuración coherente, limpieza completa del estado y definición explícita de los parámetros críticos permitieron resolver todos los fallos.
