# Docker

## 1. Introducción

Docker es una aplicación donde podemos ejecutar una función, un proceso, crear aplicaciones dentro de lo que denominamos los contenedorees.
El contenedor es un entorno asilado qie mo permite ejecutar nuestro software con las dependencias que hayamos establecido.

Los contenedores son:
- Ligeros  
- Aislados  
- Portables  
- Reproducibles
- Monolíticos
- Arquitectura de microservicios

Permiten que una aplicación funcione igual en cualquier entorno.

---

## 2. Conceptos fundamentales

### 2.1 Imagen

Una imagen es una plantilla inmutable que contiene el sistema base y todas las dependencias necesarias para ejecutar una aplicación.

Ejemplos de imágenes:

- `python:3.11`
- `node:18`
- `ubuntu:22.04`

### 2.2 Contenedor

Es una instancia en ejecución de una imagen.  
Si la imagen es una plantilla, el contenedor es el resultado funcional ejecutándose.

### 2.3 Dockerfile

Archivo de configuración que contiene las instrucciones necesarias para construir una imagen personalizada.

### 2.4 Registro de imágenes

Repositorio donde se almacenan imágenes, como:

- Docker Hub  
- GitHub Container Registry  

### 2.5 Volumen

Un volumen permite guardar datos fuera del contenedor para que no se pierdan al eliminarlo.

---

## 3. ¿Por qué usar Docker?

- Evita diferencias entre entornos de desarrollo y producción.  
- Permite ejecutar varias versiones de aplicaciones o librerías de forma aislada.  
- Facilita despliegues.  
- Es ideal para microservicios.  
- Es útil en arquitecturas distribuidas.

---

## 4. Ejemplo básico de Dockerfile

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
EXPOSE 3000
```

Explicación breve:

- `FROM`: define la imagen base.  
- `WORKDIR`: establece el directorio de trabajo.  
-
nedor.  
- `RUN`: ejecuta comandos durante la construcción.  
- `CMD`: define el comando que se ejecutará al iniciar el contenedor.  
- `EXPOSE`: documenta el puerto usado por el contenedor.

---

## 5. Comandos esenciales de Docker

### 5.1 Imágenes

```bash
docker pull nombre_imagen
docker images
docker rmi nombre_imagen
```

### 5.2 Contenedores

```bash
docker run nombre_imagen
docker ps
docker stop ID
docker rm ID
```

### 5.3 Construcción de imágenes

```bash
docker build -t nombre .
```

### 5.4 Logs del contenedor

```bash
docker logs ID
```

---

## 7. Usos comunes de Docker

- Desarrollo de aplicaciones  
- Microservicios  
- Bases de datos en contenedores  
- Entornos de prueba  
- Arquitecturas distribuidas como Kafka, Spark o Jitsi  

---

## 8. Conclusión
Docker nos va  a permitir poder conecatr todos los contenedores entre ellos para una comunicación para nuestra aplicación, además si se usa una arquitectura de 
microservicios, podríamos realizar cambios en algún contenedor sin tener la necesidad de afectar al resto.

