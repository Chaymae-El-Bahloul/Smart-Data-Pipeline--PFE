import json
import time
import numpy as np
import os
from kafka import KafkaConsumer
from sklearn.ensemble import IsolationForest

# ==============================
# PROMETHEUS IMPORTS
# ==============================
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    start_http_server
)

# ==============================
# PROMETHEUS METRICS
# ==============================
MESSAGES_RECUS = Counter(
    'kafka_messages_total',
    'Nombre total de messages reçus'
)

ANOMALIES_DETECTEES = Counter(
    'anomalies_total',
    'Nombre total d anomalies détectées'
)

TEMPERATURE_ACTUELLE = Gauge(
    'temperature_actuelle',
    'Derniere temperature recue'
)

TAILLE_HISTORIQUE = Gauge(
    'historique_taille',
    'Nombre d enregistrements'
)

MOTEUR_ACTIF = Gauge(
    'moteur_traitement',
    '0 = Pandas, 1 = Spark'
)

TEMPS_TRAITEMENT = Histogram(
    'temps_traitement',
    'Temps de traitement',
    buckets=[0.001, 0.01, 0.1, 0.5, 1]
)

KAFKA_CONNECTE = Gauge(
    'kafka_status',
    '1 = connecté, 0 = déconnecté'
)

TAUX_ANOMALIES = Gauge(
    'taux_anomalies',
    'Pourcentage anomalies'
)

# ==============================
# START PROMETHEUS SERVER
# ==============================
start_http_server(8000)
print("Prometheus running on port 8000")

# ==============================
# PATHS
# ==============================
BASE_DIR = "/app"
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

history_file = os.path.join(DATA_DIR, "history.json")
result_file = os.path.join(DATA_DIR, "last_result.json")

# ==============================
# CONNECT TO KAFKA
# ==============================
KAFKA_CONNECTE.set(0)

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
        KAFKA_CONNECTE.set(1)
        break
    except Exception as e:
        print("Kafka not ready:", e)
        KAFKA_CONNECTE.set(0)
        time.sleep(5)

# ==============================
# MODEL
# ==============================
model = IsolationForest(contamination=0.05, random_state=42)

# ==============================
# LOAD HISTORY
# ==============================
if os.path.exists(history_file):
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except:
        history = []
else:
    history = []

TAILLE_HISTORIQUE.set(len(history))

print("Consumer started...")

# for anomaly rate
last_100 = []

# ==============================
# CONSUME LOOP
# ==============================
for message in consumer:
    try:
        start = time.time()

        data = message.value
        temperature = data["temperature"]

        # metrics
        MESSAGES_RECUS.inc()
        TEMPERATURE_ACTUELLE.set(temperature)

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

        print("Processed:", data)

        # ================= METRICS =================

        if anomaly == 1:
            ANOMALIES_DETECTEES.inc()

        if data["engine"] == "Spark":
            MOTEUR_ACTIF.set(1)
        else:
            MOTEUR_ACTIF.set(0)

        TAILLE_HISTORIQUE.set(len(history))

        # anomaly rate
        last_100.append(anomaly)
        if len(last_100) > 100:
            last_100.pop(0)

        if len(last_100) > 0:
            rate = (sum(last_100) / len(last_100)) * 100
            TAUX_ANOMALIES.set(rate)

        # processing time
        duration = time.time() - start
        TEMPS_TRAITEMENT.observe(duration)

    except Exception as e:
        print("Error:", e)
	
