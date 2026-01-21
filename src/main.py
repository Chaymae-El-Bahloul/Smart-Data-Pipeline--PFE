from ingestion.ingestion import ingest_data
from preprocessing.preprocessing import preprocess
from processing.processing import process
from adaptation.adaptation import adapt
from storage.storage import store
from visualization.visualization import visualize

def main():
    # 1. Ingestion
    data = ingest_data()

    # 2. Prétraitement
    data = preprocess(data)

    # 3. Traitement
    data = process(data)

    # 4. Monitoring & auto-adaptation
    metrics = {"latency": 120}
    decision = adapt(metrics)

    if decision == "switch_to_stream":
        print("→ Adaptation appliquée : passage en mode streaming")
    else:
        print("→ Mode batch conservé")

    # 5. Stockage
    store(data)

    # 6. Visualisation
    visualize(data)

if __name__ == "__main__":
    main()
    
