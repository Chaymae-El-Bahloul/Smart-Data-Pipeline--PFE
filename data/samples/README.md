# Dossier Data

Ce dossier contient les données utilisées et générées par le système.

## history.json
- Fichier généré dynamiquement par le consumer Kafka.
- Stocke l’historique des messages IoT traités.
- Structure :
  - temperature
  - engine (Pandas ou Spark)
  - metric_used
  - anomaly (True/False)

Ce fichier peut être réinitialisé via l’interface Streamlit.

## Remarque

Les données sont simulées par le producteur Kafka afin d’imiter un flux IoT en temps réel.

