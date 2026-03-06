import json
import time
import numpy as np
import os
from kafka import KafkaConsumer
from sklearn.ensemble import IsolationForest

BASE_DIR = "/app"
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

history_file = os.path.join(DATA_DIR, "history.json")
result_file = os.path.join(DATA_DIR, "last_result.json")

# -----------------------------
# RETRY CONNECTION TO KAFKA
# -----------------------------
while True:
    try:
        consumer = KafkaConsumer(
            "pfe-data",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            group_id="iot-group",
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
        print("Connected to Kafka")
        break
    except Exception as e:
        print("Kafka not ready:", e)
        time.sleep(5)

model = IsolationForest(contamination=0.05, random_state=42)

# -----------------------------
# LOAD HISTORY
# -----------------------------
if os.path.exists(history_file):
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except:
        history = []
else:
    history = []

print("Consumer started...")

# -----------------------------
# CONSUME LOOP
# -----------------------------
for message in consumer:
    try:
        data = message.value
        temperature = data["temperature"]
        anomaly = 0

        if len(history) > 20:
            train_data = np.array(
                [h["temperature"] for h in history]
            ).reshape(-1, 1)

            model.fit(train_data)

            prediction = model.predict(
                np.array([[temperature]])
            )
            anomaly = int(prediction[0] == -1)

        data["anomaly"] = anomaly
        data["engine"] = "Pandas" if temperature < 25 else "Spark"

        history.append(data)

        with open(history_file, "w") as f:
            json.dump(history, f)

        with open(result_file, "w") as f:
            json.dump(data, f)

        print("Processed and saved:", data)

    except Exception as e:
        print("Error processing message:", e)
