import json
import time
import random
from kafka import KafkaProducer

# -----------------------------
# RETRY CONNECTION
# -----------------------------
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka")
        break
    except Exception:
        print("Kafka not ready, retrying in 5 seconds...")
        time.sleep(5)

print("Producer started...")

devices = ["device_1", "device_2", "device_3"]

while True:
    temperature = random.uniform(18, 30)

    # 5% anomaly
    if random.random() < 0.05:
        temperature = random.uniform(35, 45)

    message = {
        "device": random.choice(devices),
        "temperature": temperature,
        "humidity": random.uniform(30, 70),
        "ts": time.time()
    }

    producer.send("pfe-data", value=message)
    producer.flush()

    print("Sent:", message)

    time.sleep(1)
