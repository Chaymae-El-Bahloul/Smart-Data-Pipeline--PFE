# Smart Data Pipeline

**Conception et Implémentation d'un Pipeline de Données Intelligent et Auto-Adaptatif pour la Gestion Dynamique des Flux de Données**

[![PFE](https://img.shields.io/badge/Projet-Fin%20d'%C3%A9tudes-blue)]()
[![Statut](https://img.shields.io/badge/Statut-Termin%C3%A9-success)]()
[![Docker](https://img.shields.io/badge/Deploy-Docker%20Compose-2496ED)]()
[![License](https://img.shields.io/badge/License-Acad%C3%A9mique-lightgrey)]()

> Plateforme intelligente de monitoring de flux de données IoT en temps réel, capable de **basculer automatiquement entre Pandas et Spark** selon le volume de données, de **détecter les anomalies** par Machine Learning (Isolation Forest), et de fournir une **double couche de visualisation** : un dashboard métier (Streamlit) et une supervision technique professionnelle (Prometheus + Grafana).

---

## Sommaire

- [Présentation](#présentation)
- [Contexte du projet](#contexte-du-projet)
- [Problématique](#problématique)
- [Notions de base](#notions-de-base)
- [État de l'art](#état-de-lart)
- [Architecture du système](#architecture-du-système)
- [Couche d'ingestion — Kafka](#couche-dingestion--kafka)
- [Couche de traitement adaptatif](#couche-de-traitement-adaptatif)
- [Détection d'anomalies — Isolation Forest](#détection-danomalies--isolation-forest)
- [Visualisation métier — Streamlit](#visualisation-métier--streamlit)
- [Supervision technique — Prometheus & Grafana](#supervision-technique--prometheus--grafana)
- [Conteneurisation — Docker](#conteneurisation--docker)
- [Flux de données complet](#flux-de-données-complet)
- [Résultats et performances](#résultats-et-performances)
- [Environnement de test](#environnement-de-test)
- [Limites du système](#limites-du-système)
- [Installation et déploiement](#installation-et-déploiement)
- [Structure du dépôt](#structure-du-dépôt)
- [Dataset utilisé](#dataset-utilisé)
- [Perspectives](#perspectives)
- [Bibliographie](#bibliographie)
- [Auteures & encadrement](#auteures--encadrement)

---

## Présentation

**Smart Data Pipeline** est un projet de fin d'études (PFE) de la filière DUT Ingénierie des Données, réalisé à l'**EST El Kelâa des Sraghna — Université Cadi Ayyad**. Le projet porte sur la conception d'une plateforme intelligente capable d'ingérer, traiter, analyser et visualiser un flux de données IoT en temps réel, tout en s'adaptant dynamiquement à la charge entrante.

| | |
|---|---|
| **Type** | Projet de Fin d'Études (PFE) |
| **Soutenance** | 16 Juin 2026 |
| **Établissement** | EST El Kelâa des Sraghna — Université Cadi Ayyad |
| **Filière** | DUT Ingénierie des Données |
| **Auteures** | BOUDALLAA Samah · EL BAHLOUL Chaymae · EL BASRI Khadija |
| **Encadrant pédagogique** | Pr. Anas Berka |
| **Examinateur** | Pr. Soufiane Mouchtabih |
| **Code source** | [github.com/Samah-boudallaa/smart-data-pipeline-pfe](https://github.com/Samah-boudallaa/smart-data-pipeline-pfe) (privé) |

### Points clés du projet

| Caractéristique | Détail |
|---|---|
| Moteur adaptatif | Bascule automatique **Pandas ↔ Spark** selon le volume |
| Détection d'anomalies | **Isolation Forest** (Machine Learning) |
| Ingestion | **Apache Kafka 3.7.0** (mode KRaft) |
| Dashboard métier | **Streamlit** (port 8501) — thème clair/sombre |
| Supervision technique | **Prometheus** (port 9090) + **Grafana** (port 3000) |
| Déploiement | **Docker Compose** — une seule commande |
| Dataset | IoT Telemetry Data (Kaggle, ~132K mesures) |
| Latence d'ingestion | **< 100 ms** en local |
| Taux d'anomalies observé | **4–5 %** du flux entrant |
| Durée moyenne de traitement | **< 500 ms** par message |

---

## Contexte du projet

### Introduction générale

L'explosion des données numériques générées par les entreprises, réseaux sociaux, systèmes IoT et applications web a conduit à une croissance exponentielle du volume d'informations à traiter — au cœur du phénomène **Big Data**. Les systèmes traditionnels montrent leurs limites face à ces besoins en termes de **scalabilité**, de **latence** et de **traitement en temps réel**.

Les pipelines classiques, souvent **statiques**, sont peu adaptés aux variations de charge, entraînant dégradation des performances et mauvaise utilisation des ressources.

### Problématique

> **Comment concevoir un pipeline capable de s'adapter automatiquement aux variations des flux tout en garantissant des performances stables ?**

Le projet vise à concevoir un **pipeline intelligent et auto-adaptatif**, capable de gérer efficacement des flux dynamiques tout en maintenant des performances optimales.

---

## Notions de base

### Big Data — les 5V

| V | Signification |
|---|---|
| **Volume** | quantité massive de données générées chaque jour |
| **Vélocité** | vitesse de production et de traitement des données |
| **Variété** | formats hétérogènes (structurées, semi-structurées, non structurées) |
| **Véracité** | qualité et fiabilité des données |
| **Valeur** | capacité à extraire des informations pertinentes |

### Data Pipeline

Architecture permettant de **déplacer, transformer et stocker** des données automatiquement, depuis les sources jusqu'aux systèmes d'analyse. Composants principaux : sources de données (bases, APIs, capteurs), moteurs de traitement, systèmes de stockage/visualisation.

### Batch vs Streaming

| Critère | Batch | Streaming |
|---|---|---|
| Latence | Élevée | Faible |
| Usage | Analytique | Temps réel |
| Complexité | Moyenne | Élevée |

> Dans ce projet, le **streaming** est privilégié afin de répondre aux exigences de réactivité.

### Pipelines intelligents et auto-adaptatifs

Un pipeline intelligent analyse son propre fonctionnement et ajuste automatiquement ses paramètres selon les métriques observées :

- **Collecte de métriques** : latence, débit, taux d'erreur
- **Comparaison avec des objectifs de service** (SLA/SLO)
- **Ajustement automatique** des ressources et configurations

---

## État de l'art

### Comparaison des architectures de traitement

| Architecture | Principe | Exemple / Créateur | Avantages | Inconvénients | Adaptée pour |
|---|---|---|---|---|---|
| **Batch** | Traitement différé en lots | Hadoop | Traitement massif, robustesse | Latence élevée, non temps réel | Analyses historiques, reporting |
| **Lambda** | Batch + temps réel + couche de service | Nathan Marz | Précision, faible latence | Complexité, maintenance lourde | Systèmes nécessitant précision + rapidité |
| **Kappa** | Traitement continu uniquement (streaming) | Jay Kreps / Apache Kafka | Simplicité, cohérence, temps réel | Moins adapté aux volumes historiques massifs | Applications temps réel, événements |

### Plateformes et outils retenus

| Outil | Rôle | Avantages | Limites |
|---|---|---|---|
| **Apache Kafka** | Streaming distribué (Producer → Broker → Consumer) | Haute scalabilité, tolérance aux pannes, faible latence | Complexité de configuration |
| **Apache Spark** | Traitement distribué (Core, SQL, Streaming, MLlib) | Traitement rapide en mémoire, agrégations massives | Consommation mémoire élevée |
| **pandas** | Manipulation de données tabulaires Python | Simple, rapide pour petits volumes | Non distribué |
| **Stream Processing** | Analyse dès l'arrivée des données | Latence faible, traitement événementiel | Nécessite infrastructure streaming |
| **Streamlit** | Visualisation interactive métier | Développement rapide, interface intuitive | Non adapté aux très gros datasets |
| **Prometheus** | Collecte de métriques en séries temporelles | Léger, scraping HTTP natif, PromQL puissant | Métriques numériques uniquement |
| **Grafana** | Visualisation et dashboards de métriques | Dashboards interactifs, alertes configurables | Nécessite une source externe |
| **Docker** | Conteneurisation et déploiement | Portabilité, isolation, reproductibilité | Apprentissage des conteneurs requis |

### Positionnement du projet

Le projet adopte :
- Une architecture inspirée du **modèle Kappa**
- **Kafka** pour l'ingestion
- Un **moteur adaptatif** (Pandas ou Spark)
- **Streamlit** pour la visualisation métier
- **Prometheus et Grafana** pour la supervision technique
- **Docker** pour la conteneurisation

Réponses aux exigences : temps réel, modularité, évolutivité, observabilité, simplicité d'exploitation.

---

## Architecture du système

L'architecture est organisée en couches fonctionnelles assurant le cycle de vie complet des données : **ingestion → traitement → analyse → stockage → visualisation → supervision**.

```
IoT Sensors / Web Apps / Social Media / Databases
                    │
                    ▼
              Kafka (Ingestion)
                    │
                    ▼
        Adaptive Processing Engine
        ┌─────────────────────────┐
        │  Apache Spark (Stream/Batch) │
        │  pandas (Data Analysis)      │
        └─────────────────────────┘
                    │
                    ▼
       Visualization & Monitoring
   ┌────────────┬────────────┬────────────┐
   │ Streamlit  │ Prometheus │  Grafana   │
   │ (Dashboards)│ (Metrics) │(Monitoring)│
   └────────────┴────────────┴────────────┘
                    │
                    ▼
          Docker (Conteneurisation)
```

### Sources de données

Les données proviennent d'une **simulation de capteurs IoT** basée sur le dataset public **IoT Telemetry Data** (Kaggle) — température, humidité, pression atmosphérique, monoxyde de carbone (CO), fumée et GPL, enregistrées à intervalles réguliers. Les données sont générées sous forme de **messages JSON**, transmis par un script Python jouant le rôle de producteur.

---

## Couche d'ingestion — Kafka

La couche d'ingestion reçoit et distribue les flux de données. Les messages sont publiés dans un **topic Kafka**, ce qui permet :

- de gérer un flux continu de données,
- de découpler producteurs et consommateurs,
- d'assurer une transmission fiable des messages.

Un **consumer Kafka** développé en Python récupère les données publiées et les transmet aux modules de traitement, garantissant un traitement **asynchrone et scalable**.

---

## Couche de traitement adaptatif

Deux moteurs de traitement permettent d'adapter dynamiquement le système au volume de données reçu.

### Moteur Pandas (petits volumes)

- Nettoyage des données
- Transformation des variables
- Calcul de statistiques simples
- Préparation des données pour l'analyse

### Moteur Spark (gros volumes)

- Traitement de volumes importants
- Calculs distribués
- Amélioration de la scalabilité

### Moteur d'adaptation intelligent

Un module de décision automatique analyse :

- le **volume de données**,
- la **fréquence d'arrivée des messages**,
- les **performances du traitement**,

et sélectionne automatiquement le moteur le plus approprié.

### Résultats du traitement adaptatif

| Volume de données | Moteur sélectionné | Temps moyen de traitement |
|---|---|---|
| < 10 000 lignes | Pandas | Très rapide (< 1 s) |
| > 50 000 lignes | Spark | Plus stable et scalable |

---

## Détection d'anomalies — Isolation Forest

Un module d'analyse basé sur l'algorithme **Isolation Forest** (Machine Learning) permet :

- d'identifier des comportements inhabituels,
- de détecter des valeurs aberrantes dans les flux,
- d'améliorer la surveillance des systèmes IoT.

Les résultats sont ajoutés aux données traitées et exploités par le module de visualisation. Les données enrichies sont stockées dans un fichier **JSON historique** (`history.json`), mis à jour dynamiquement à chaque analyse.

---

## Visualisation métier — Streamlit

L'application **Streamlit** (port **8501**) constitue le tableau de bord interactif métier permettant de :

- afficher les données reçues en temps réel,
- visualiser les statistiques générées par le pipeline,
- détecter visuellement les anomalies,
- basculer entre thème **sombre** et **clair**,
- configurer l'intervalle de rafraîchissement et la sensibilité de détection des anomalies,
- confirmer la réinitialisation des données.

---

## Supervision technique — Prometheus & Grafana

### Prometheus (port 9090)

Le consumer expose un endpoint HTTP (`:8000/metrics`) via la bibliothèque `prometheus_client`, scrapé toutes les **15 secondes**. Métriques exposées :

| Métrique | Description |
|---|---|
| `kafka_messages_total` | Nombre total de messages reçus depuis Kafka |
| `anomalies_total` | Nombre total d'anomalies détectées par Isolation Forest |
| `iot_temperature_celsius` | Dernière valeur de température reçue |
| `taux_anomalies_percent` | Pourcentage d'anomalies sur les 100 derniers messages |
| `moteur_traitement` | Moteur actif (0 = Pandas, 1 = Spark) |
| `historique_taille` | Nombre d'enregistrements dans le fichier historique |
| `traitement_duree_secondes` | Durée de traitement de chaque message |
| `kafka_connection_status` | État de la connexion au broker Kafka |

### Grafana (port 3000)

Connecté à Prometheus comme source de données, le dashboard se rafraîchit automatiquement toutes les **5 secondes** et présente :

| Panneau | Description |
|---|---|
| Statut Kafka | Indicateur binaire Connecté/Déconnecté avec code couleur |
| Messages reçus | Compteur cumulatif de messages Kafka traités |
| Anomalies détectées | Compteur total avec seuils colorés (vert/orange/rouge) |
| Taux d'anomalies | Pourcentage avec alertes visuelles par seuils |
| Moteur actif | Affiche Pandas ou Spark selon le basculement |
| Température IoT (jauge) | Thermomètre circulaire, zones colorées 0–60 °C |
| Évolution température | Série temporelle en degrés Celsius |
| Taux messages/sec | Débit instantané via la fonction `rate()` de Prometheus |
| Durée de traitement | Durée moyenne calculée à partir de l'histogramme |

---

## Conteneurisation — Docker

Chaque composant est encapsulé dans un **conteneur Docker**, ce qui permet d'isoler les services, d'assurer la portabilité et de faciliter la reproduction de l'environnement.

| Conteneur | Rôle |
|---|---|
| Kafka | Gestion des flux de messages |
| Spark | Traitement distribué |
| Application Python | Traitement et analyse |
| Streamlit | Interface utilisateur métier |
| Prometheus | Collecte des métriques |
| Grafana | Visualisation des métriques système |

L'ensemble est orchestré via **Docker Compose**, permettant de lancer toute la plateforme en une seule commande.

---

## Flux de données complet

```
IoT Sensors (Simulation Dataset)
        │
        ▼
   Producer (Python)
        │
        ▼
     Kafka (Topic)
        │
        ▼
 Moteur Adaptatif (Pandas / Spark) ──► Stockage (JSON)
        │
        ▼
   Module IA (Anomalies)
        │
        ├──► Consumer ──► Streamlit (Dashboard)
        │
        └──► Prometheus ──► Grafana
```

**Étapes du pipeline :**

1. Les capteurs IoT simulés génèrent des données → producteur Kafka
2. Le producteur publie les messages dans un topic Kafka
3. Le consommateur Kafka récupère les messages → module de traitement
4. Le moteur adaptatif sélectionne Pandas ou Spark selon la charge
5. Les données sont analysées par le module de détection d'anomalies (IA)
6. Les résultats sont enregistrés dans un fichier JSON historique
7. Streamlit lit ces données et les affiche dans un tableau de bord interactif
8. Prometheus collecte les métriques exposées par le consumer et les transmet à Grafana
9. Les métriques (messages traités, anomalies, température, durée de traitement) sont visualisées en temps réel dans Grafana

---

## Résultats et performances

### Validation de l'ingestion

- Messages reçus **sans perte**
- Latence **< 100 ms** en local
- Support de l'envoi simultané de plusieurs messages

### Métriques observées en production (tests)

| Métrique | Valeur observée | Signification |
|---|---|---|
| `kafka_messages_total` | 28 400+ | Messages traités depuis le démarrage |
| `anomalies_total` | 1 460+ | Anomalies détectées au total |
| `taux_anomalies_percent` | 4–5 % | Taux stable et conforme aux attentes |
| `iot_temperature_celsius` | 20–40 °C | Plage normale des capteurs IoT |
| `moteur_traitement` | 1 (Spark) | Basculement vers Spark confirmé |
| `kafka_connection_status` | 1 | Connexion Kafka active |

### Performances de traitement

- **Pandas** plus rapide pour les petits volumes
- **Spark** plus performant à mesure que le volume augmente
- Durée moyenne de traitement (`traitement_duree_secondes`) : **< 500 ms** pour la majorité des messages

### Scalabilité

Le système peut évoluer horizontalement grâce à :
- la nature distribuée de Kafka,
- le traitement parallèle de Spark,
- la conteneurisation Docker.

> Les tests ont été réalisés en environnement **local**, ce qui limite la simulation d'un cluster réel.

### Discussion

1. L'architecture est **fonctionnelle et stable**
2. Le système répond aux **exigences initiales**
3. L'approche adaptative **améliore l'efficacité**
4. Les conteneurs **simplifient le déploiement**
5. Prometheus + Grafana apportent une **observabilité complète** du pipeline

Comparativement à une architecture sans supervision, la solution offre : visibilité complète sur l'état interne, détection proactive des dysfonctionnements, traçabilité historique des métriques.

### Apport du monitoring

- **Observabilité** : toutes les métriques clés visibles en un seul endroit
- **Réactivité** : rafraîchissement automatique (5 s) pour détecter rapidement toute dégradation
- **Professionnalisme** : utilisation d'outils standards de l'industrie
- **Extensibilité** : nouvelles métriques ajoutables facilement dans le consumer Python

---

## Environnement de test

| Composant | Détail |
|---|---|
| Système d'exploitation | Ubuntu (WSL) |
| Conteneurisation | Docker & Docker Compose |
| Broker de messages | Apache Kafka 3.7.0 (mode KRaft) |
| Langage | Python 3.10 |
| Bibliothèques | `kafka-python`, `pandas`, `pyspark`, `prometheus_client` |
| Interface utilisateur | Streamlit (port 8501) |
| Supervision | Prometheus (port 9090), Grafana (port 3000) |
| Machine locale | 16 Go RAM, processeur i5 |

---

## Limites du système

- Tests réalisés **uniquement en local**
- Absence d'un **cluster Spark distribué réel**
- Pas d'intégration avec une **base de données persistante**
- **Sécurité non implémentée** (authentification Kafka)
- Les **alertes Grafana** n'ont pas été configurées dans le cadre de ce projet

---

## Installation et déploiement

### Prérequis

- Docker & Docker Compose
- Python 3.10+ (pour exécution hors conteneur, si besoin)

### Déploiement complet

```bash
# 1. Cloner le dépôt
git clone https://github.com/Samah-boudallaa/smart-data-pipeline-pfe.git
cd smart-data-pipeline-pfe

# 2. Lancer l'ensemble de la plateforme
docker-compose up --build
```

Cette commande initialise et démarre automatiquement :
- le système de messagerie **Kafka**,
- les services de **traitement des données** (producer, consumer, moteur adaptatif),
- l'interface de visualisation **Streamlit**,
- les outils de supervision **Prometheus** et **Grafana**.

### Accès aux services

| Service | URL |
|---|---|
| Dashboard métier (Streamlit) | http://localhost:8501 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Métriques brutes du consumer | http://localhost:8000/metrics |

### Vérification rapide

```promql
up{job="smart-pipeline-consumer"}
```
> Doit retourner la valeur `1`, confirmant que le service est correctement supervisé.

---

## Structure du dépôt

```
smart-data-pipeline-pfe/
│
├── data/                        # Données et dataset IoT
│
├── docs/                        # Documentation du projet
│
├── src/                         # Code source principal (producer, consumer,
│                                 #   moteur adaptatif, détection d'anomalies)
│
├── .dockerignore                # Fichiers exclus de Docker
├── .gitignore                   # Fichiers exclus de Git
│
├── Dockerfile.app                # Image Docker de l'application Streamlit
├── Dockerfile.consumer           # Image Docker du consommateur Kafka
├── Dockerfile.producer           # Image Docker du producteur Kafka
│
├── app.py                        # Application Streamlit (dashboard métier)
├── docker-compose.yml            # Orchestration des conteneurs
├── prometheus.yml                # Configuration de Prometheus
├── requirements.txt              # Dépendances Python (app + consumer)
├── requirements_producer.txt     # Dépendances Python (producteur)
└── README.md                     # Documentation principale
```

### Description des composants principaux

| Fichier / Dossier | Description |
|---|---|
| `data/` | Dataset IoT Telemetry Data + fichiers JSON historiques générés |
| `docs/` | Documentation technique (schémas d'architecture, notes) |
| `src/` | Modules : producteur Kafka, consommateur, moteur adaptatif, détection d'anomalies |
| `app.py` | Tableau de bord interactif Streamlit (visualisation métier temps réel) |
| `prometheus.yml` | Configuration des cibles de scraping Prometheus |
| `Dockerfile.app` | Image Docker du service applicatif (dashboard Streamlit) |
| `Dockerfile.consumer` | Image Docker du consommateur Kafka |
| `Dockerfile.producer` | Image Docker du producteur Kafka |
| `docker-compose.yml` | Orchestration de l'ensemble des services, réseaux et volumes |
| `requirements.txt` | Dépendances Python pour l'application et le consommateur |
| `requirements_producer.txt` | Dépendances Python spécifiques au producteur Kafka |

> **Historique de développement** : le dépôt compte **58 commits** répartis sur **2 branches**, témoignant d'un développement itératif et rigoureux mené via Git/GitHub.

---

## Dataset utilisé

### IoT Telemetry Data (Kaggle)

| Champ | Valeur |
|---|---|
| Nom | IoT Telemetry Data |
| Source | Kaggle |
| Format | CSV |
| Nombre de colonnes | 9 |
| Type de données | Mesures de capteurs IoT |
| Lien | [kaggle.com/datasets/garystafford/environmental-sensor-data-132k](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k) |

### Description des colonnes

| Colonne | Type | Description |
|---|---|---|
| `ts` | timestamp (float) | Horodatage Unix de la mesure |
| `device` | string | Identifiant unique du capteur IoT |
| `co` | float | Concentration en monoxyde de carbone (CO) |
| `humidity` | float | Taux d'humidité relative (%) |
| `light` | boolean | Présence ou absence de lumière ambiante |
| `lpg` | float | Concentration en gaz de pétrole liquéfié (GPL) |
| `motion` | boolean | Détection de mouvement |
| `smoke` | float | Concentration en fumée |
| `temp` | float | Température ambiante (°C) |

### Extrait du dataset

| device | temp | humidity | co | lpg | smoke | motion |
|---|---|---|---|---|---|---|
| b8:27:eb:bf:9d:51 | 22.7 | 51.0 | 0.00468 | 0.00762 | 0.01975 | false |
| 00:0f:00:70:91:0a | 19.7 | 46.0 | 0.00414 | 0.00675 | 0.01748 | false |
| b8:27:eb:bf:9d:51 | 23.1 | 52.0 | 0.00485 | 0.00790 | 0.02047 | true |

### Utilisation dans le pipeline

- Les enregistrements CSV sont lus séquentiellement par le **producteur Kafka** pour simuler un flux continu
- Les colonnes numériques (`temp`, `humidity`, `co`, `lpg`, `smoke`) alimentent le moteur de traitement adaptatif (Pandas/Spark)
- Ces mêmes colonnes sont les variables d'entrée du modèle **Isolation Forest**
- `temp` est exposée comme métrique Prometheus (`iot_temperature_celsius`) et visualisée dans Grafana
- Les résultats enrichis sont stockés dans `history.json` et affichés sur le dashboard Streamlit

---

## Perspectives

- **Auto-scalabilité** : intégration de **Kubernetes** pour gérer dynamiquement les conteneurs et améliorer la disponibilité
- **Modèles IA avancés** : réseaux de neurones profonds ou modèles de détection d'anomalies plus sophistiqués
- **Base de données distribuée** : Apache Cassandra ou Elasticsearch pour le stockage et l'analyse à grande échelle des données historiques
- **Alertes automatiques Grafana** et analyse des tendances sur de longues périodes
- **Application à des scénarios réels** : surveillance d'infrastructures IoT, Smart Cities, suivi de systèmes industriels

---

## Bibliographie

1. IBM, *What is Big Data?*, IBM Documentation.
2. N. Marz & J. Warren, *Big Data: Principles and best practices of scalable realtime data systems*, Manning, 2015.
3. DZone, *What is a Data Pipeline?*
4. S. Sagiroglu & D. Sinanc, *Big Data: A Review*, IEEE ICCTS, 2013.
5. Talend, *Data Pipeline Definition*.
6. Google Cloud, *Batch vs Streaming Data Processing*.
7. M. Chen, S. Mao & Y. Liu, *Big Data: A Survey*, Mobile Networks and Applications, 2014.
8. Apache Kafka Documentation. https://kafka.apache.org/documentation/
9. Apache Spark Streaming Guide.
10. S. Xie et al., *Adaptive Data Pipelines: Techniques and Applications*, IEEE Xplore, 2020.
11. J. Kreps, *Questioning the Lambda Architecture*.
12. Q. Zhang, M. Chen et al., *Challenges in Big Data Processing Systems*, IEEE, 2018.
13. Apache Spark Documentation.
14. Git Documentation — Version Control Best Practices.
15. Streamlit Documentation. https://docs.streamlit.io/
16. Prometheus Authors, *Prometheus Documentation*.
17. Grafana Labs, *Grafana Documentation*.
18. R. Rajkumar, I. Lee, L. Sha & J. Stankovic, *Cyber-Physical Systems: The Next Computing Revolution*, DAC, 2010.
19. B. Gregg, *Systems Performance: Enterprise and the Cloud*, Prentice Hall, 2013.
20. C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006.
21. Docker Documentation officielle.
22. Docker Compose Documentation.
23. Pandas Documentation.
24. M. Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
25. J. Densmore, *Data Pipelines Pocket Reference*, O'Reilly Media, 2021.
26. A. Psaltis, *Streaming Data: Understanding the real-time pipeline*, Manning, 2016.
27. F. T. Liu, K. M. Ting & Z.-H. Zhou, *Isolation-Based Anomaly Detection*, ACM TKDD, 2012.
28. G. Stafford, *IoT Telemetry Data*, Kaggle Dataset, 2020.
29. BOUDALLAA S., EL BAHLOUL C., EL BASRI K., *smart-data-pipeline-pfe — Code source du projet*, GitHub, 2026.

---

## Auteures & encadrement

| Rôle | Nom |
|---|---|
| Auteure | BOUDALLAA Samah |
| Auteure | EL BAHLOUL Chaymae |
| Auteure | EL BASRI Khadija |
| Encadrant pédagogique | Pr. Anas Berka — EST El Kelâa des Sraghna |
| Examinateur | Pr. Soufiane Mouchtabih — EST El Kelâa des Sraghna |

EST El Kelâa des Sraghna — Université Cadi Ayyad
Filière DUT : Ingénierie des données

---

*Année universitaire 2025–2026*
