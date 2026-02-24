from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="localhost:9092")

with open("images/input/animal.jpeg", "rb") as f:
    data = f.read()

producer.send("frames_raw", value=data)
producer.flush()

print("Imagen enviada:", len(data), "bytes")
