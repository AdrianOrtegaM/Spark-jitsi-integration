# Configuración Dominant Speaker en Jitsi

Para activar el modo de hablante dominante en Jitsi y permitir que la persona que está hablando aparezca automáticamente en la vista principal de la videollamada, se debe modificar la configuración del contenedor de Jitsi.

## Pasos

Acceder directamente al contenedor de Jitsi:

```bash
docker exec -it jitsimeet-web-1 bash
```

Editar el archivo de configuración:

```bash
nano /config/config.js
```

Añadir al final del archivo:

```js
config.disableTileView = true;
config.startVideoMuted = 1;
config.startAudioMuted = 1;
```

Guardar y salir:

CTRL + O → Enter → CTRL + X

Salir del contenedor:

```bash
exit
```

Reiniciar Jitsi:

```bash
docker restart jitsimeet-web-1
```

## Resultado

El sistema activará el modo de hablante dominante (dominant speaker), haciendo que la persona que habla en cada momento aparezca automáticamente en la vista principal de la videollamada.
