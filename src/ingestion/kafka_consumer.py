from kafka import KafkaConsumer
import json

from preprocessing import preprocess
from processing import process
from storage import store

consumer = KafkaConsumer(
    'pfe-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer + Pipeline démarré...")

for message in consumer:
    raw_data = message.value
    print("Reçu :", raw_data)

    data = preprocess(raw_data)
    if data is None:
        continue

    data = process(data)
    store(data)
