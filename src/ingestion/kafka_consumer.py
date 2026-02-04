from kafka import KafkaConsumer
import json
import pandas as pd

def consume_from_kafka(topic='pfe-data', max_messages=5):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    data = []
    for message in consumer:
        data.append(message.value)
        if len(data) >= max_messages:
            break

    consumer.close()
    return pd.DataFrame(data)
