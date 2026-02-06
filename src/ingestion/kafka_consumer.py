from kafka import KafkaConsumer
import json
from src.processing import process_with_spark

consumer = KafkaConsumer(
    'pfe-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='pfe-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer Kafka démarré (ingestion uniquement)...")

for message in consumer:
    data = message.value
    print(f"\nMessage reçu depuis Kafka : {data}")

    process_with_spark(data)

