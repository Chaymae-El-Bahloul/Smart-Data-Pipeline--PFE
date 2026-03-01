import json
import pandas as pd
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Lecture du dataset IoT...")

df = pd.read_csv("data/iot_telemetry_data.csv")

print("Colonnes détectées :", df.columns)

for i, row in df.iterrows():
    message = {
        "id": int(i),
        "value": float(row["temp"])
    }

    producer.send("pfe-data", message)
    print("Message envoyé :", message)

    time.sleep(0.5)

producer.flush()
print("Envoi terminé.")

