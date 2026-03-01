from kafka import KafkaConsumer
import json
import os
import tempfile

consumer = KafkaConsumer(
    'pfe-data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

history_file = "data/history.json"

if not os.path.exists(history_file):
    with open(history_file, "w") as f:
        json.dump([], f)

for message in consumer:
    data = message.value

    temperature = data["value"]
    data["temperature"] = temperature

    if temperature < 25:
        data["engine"] = "Pandas"
        data["metric_used"] = "Low Temperature"
    else:
        data["engine"] = "Spark"
        data["metric_used"] = "High Temperature"

    data["anomaly"] = temperature > 30

    try:
        with open(history_file, "r") as f:
            history = json.load(f)
            if not isinstance(history, list):
                history = []
    except:
        history = []

    history.append(data)

    try:
        with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
            json.dump(history, tmp)
            temp_name = tmp.name

        os.replace(temp_name, history_file)
    except Exception as e:
        print("Erreur écriture:", e)

    print("Processed:", data)
