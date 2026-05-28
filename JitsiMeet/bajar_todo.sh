#!/bin/bash

set -e

echo "Bajando Spark..."
cd /home/ortis/Documentos/spark
docker compose down

echo "Bajando Jitsi..."
cd /home/ortis/Documentos/JitsiMeet
docker compose down

echo "Bajando Kafka..."
cd /home/ortis/Documentos/kafka-docker
docker compose down

echo "Bajando RTPM-Server"
cd /home/ortis/Documentos/rtmp-server
docker compose down

echo "Todo apagado correctamente."
