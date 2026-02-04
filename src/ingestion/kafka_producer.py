from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data_stream = [
    {"id": 1, "value": 120},
    {"id": 2, "value": 340},
    {"id": 3, "value": 560},
    {"id": 4, "value": 890}
]

for record in data_stream:
    producer.send('pfe-data', record)
    print("Message envoyé :", record)
    time.sleep(1)

producer.flush()
producer.close()
