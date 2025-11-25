# Apache Zookeeper

## 1. Introducción
Apache Zookeeper es un servicio que centraliza la coordinación de sistemas que están distribuidos.  
Ofrece un almacenamiento ágil, compacto y seguro para los datos que requieren ser compartidos por diversos servicios. 

Kafka utiliza Zookeeper para:
- Registrar los brokers
- Gestionar las particiones
- Supervisar el estado del clúster

---

## 2. ¿Qué problema resuelve Zookeeper?

En un sistema distribuido, muchos servicios necesitan:
- Descubrir otros servicios
- Sincronizar estados
- Elegir líderes
- Guardar configuraciones compartidas

Zookeeper proporciona:
- Consistencia
- Coordinación
- Tolerancia a fallos

---

## 3. Conceptos fundamentales

### 3.1 ZNode
Un **ZNode** es un nodo dentro del árbol de Zookeeper.
Puede ser:
- Persistente
- Temporal (desaparece al desconectar el cliente)

### 3.2 Ensemble
Conjunto de servidores Zookeeper (3, 5 o 7 nodos).

### 3.3 Leader y Followers
Un nodo actúa como **líder**, el resto como **followers**.

### 3.4 Watches
Permiten “vigilar” cambios en un nodo.

---

## 4. Uso de Zookeeper en Kafka y otros sistemas

### Kafka lo usa para:
- Registrar brokers
- Guardar la distribución de particiones
- Elegir líderes
- Detectar fallos

### Otros sistemas lo usan para:
- Configuraciones compartidas
- Descubrimiento de servicios
- Elección de líderes
- Bloqueos distribuidos

---

## 5. Ejemplo de configuración mínima en Docker Compose

```yaml
version: "3.9"

services:
  zookeeper:
    image: zookeeper:3.7
    ports:
      - "2181:2181"
```

---

## 6. Comandos básicos

### Conectarse al cliente
```bash
zkCli.sh -server localhost:2181
```

### Listar nodos
```bash
ls /
```

### Crear un nodo
```bash
create /miNodo "hola"
```

### Leer un nodo
```bash
get /miNodo
```

### Borrar un nodo
```bash
delete /miNodo
```

---

## 7. Relación con el proyecto

Zookeeper es esencial en este proyecto porque:
- Kafka lo necesita para funcionar correctamente
- Coordina el sistema distribuido
- Permite tolerancia a fallos
- Mantiene el estado de los servicios

---

## 8. Conclusión

Zookeeper es un componente fundamental para la coordinación en sistemas distribuidos.
En este proyecto asegura que Kafka funcione de forma estable, escalable y tolerante a fallos.

