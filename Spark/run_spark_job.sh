#!/bin/bash

echo "Lanzando Spark job que lee Kafka..."

docker exec -it spark-master /opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /jobs/spark_kafka_frames.py
