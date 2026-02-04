from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'pfe-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer démarré...")

for message in consumer:
    data = message.value
    print("Message reçu :", data)
